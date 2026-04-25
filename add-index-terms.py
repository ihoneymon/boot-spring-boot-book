#!/usr/bin/env python3
"""
AsciiDoc 인덱스 마커 삽입 스크립트

동작:
1. 섹션 헤딩(=== / ====)에서 용어 추출 → 헤딩 바로 다음 줄에 (((term))) 삽입
2. 주요 기술 용어(애너테이션·클래스)의 파일 내 첫 등장 위치에 indexterm 삽입
3. 이미 마커가 있는 줄은 건너뜀
"""

import re
import sys
from pathlib import Path

# 애너테이션/클래스 → 인덱스 주 항목 매핑
# (backtick 패턴, primary, secondary)
TECH_TERMS = [
    # 핵심 애너테이션
    (r'`@SpringBootApplication`', '@SpringBootApplication', '핵심 애너테이션'),
    (r'`@EnableAutoConfiguration`', '@EnableAutoConfiguration', '자동 설정'),
    (r'`@Configuration`',          '@Configuration',          '구성 클래스'),
    (r'`@Bean`',                   '@Bean',                   '빈 등록'),
    (r'`@Component`',              '@Component',              '컴포넌트'),
    (r'`@ComponentScan`',          '@ComponentScan',          '컴포넌트 스캔'),
    (r'`@Conditional`',            '@Conditional',            '조건부 설정'),
    (r'`@ConditionalOnMissingBean`','@ConditionalOnMissingBean','자동 설정'),
    (r'`@ConfigurationProperties`','@ConfigurationProperties','외부 설정'),
    (r'`@Value`',                  '@Value',                  '속성 주입'),
    (r'`@Profile`',                '@Profile',                '프로파일'),
    (r'`@SpringBootTest`',         '@SpringBootTest',         '테스트'),
    (r'`@WebMvcTest`',             '@WebMvcTest',             '테스트'),
    (r'`@DataJpaTest`',            '@DataJpaTest',            '테스트'),
    (r'`@RestController`',         '@RestController',         'Web MVC'),
    (r'`@RequestMapping`',         '@RequestMapping',         'Web MVC'),
    # 핵심 클래스
    (r'`SpringApplication`',       'SpringApplication',       '애플리케이션 실행'),
    (r'`ApplicationContext`',      'ApplicationContext',       '애플리케이션 컨텍스트'),
    (r'`Environment`',             'Environment',             '환경 설정'),
    (r'`DataSource`',              'DataSource',              '데이터 소스'),
    (r'`RestTemplate`',            'RestTemplate',            'REST 클라이언트'),
    (r'`WebClient`',               'WebClient',               'REST 클라이언트'),
    (r'`RestTemplateBuilder`',     'RestTemplateBuilder',     'REST 클라이언트'),
    (r'`ObjectMapper`',            'ObjectMapper',            'JSON'),
    (r'`HealthIndicator`',         'HealthIndicator',         '액츄에이터'),
    (r'`WebMvcConfigurer`',        'WebMvcConfigurer',        'Web MVC'),
    (r'`FilterRegistrationBean`',  'FilterRegistrationBean',  '서블릿'),
    # 설정 파일
    (r'`application\.properties`', 'application.properties',  '외부 설정'),
    (r'`application\.yml`',        'application.yml',          '외부 설정'),
    (r'`META-INF/spring\.factories`','META-INF/spring.factories','자동 설정'),
]

# 섹션 헤딩에서 인덱스 용어로 변환 시 제거할 AsciiDoc 속성 패턴
ATTR_RE      = re.compile(r'\{[a-z][a-z0-9\-]*\}')
CODE_RE      = re.compile(r'``?([^`]+?)``?')   # 단일·이중 백틱 모두 처리
BOLD_RE      = re.compile(r'\*\*?([^*]+?)\*\*?')  # *bold* / **bold**
ITALIC_RE    = re.compile(r'__?([^_]+?)__?')       # _italic_ / __italic__
LINK_RE      = re.compile(r'link:[^\[]+\[([^\]]*)\]')

# 이미 indexterm이 있는 줄 감지
INDEXTERM_RE = re.compile(r'\(\(\(|\)\)\)|indexterm:\[')


def clean_heading(text: str) -> str:
    """헤딩 텍스트에서 AsciiDoc 인라인 마크업을 모두 제거하여 순수 텍스트 반환."""
    text = LINK_RE.sub(r'\1', text)   # link:...[label] → label
    text = CODE_RE.sub(r'\1', text)   # ``term`` / `term` → term
    text = BOLD_RE.sub(r'\1', text)   # **bold** / *bold* → bold
    text = ITALIC_RE.sub(r'\1', text) # __italic__ / _italic_ → italic
    text = ATTR_RE.sub('', text)      # {attr} 제거
    # 괄호류는 공백으로 치환 (단어 붙음 방지: "파비콘(Favicon)" → "파비콘 Favicon")
    text = re.sub(r'[(){}\[\]]', ' ', text)
    # 나머지 특수문자 제거 (백틱, 별표, 언더스코어, 따옴표)
    text = re.sub(r'[`*_\'"<>]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def heading_level(line: str) -> int:
    """=== → 3, ==== → 4, 아니면 0 반환."""
    m = re.match(r'^(={2,})\s', line)
    return len(m.group(1)) if m else 0


def make_primary_indexterm(text: str) -> str:
    return f'(((({text}))))'  # 잘못된 중첩 방지를 위해 아래에서 단일로 사용


def process_file(path: Path) -> bool:
    """파일에 인덱스 마커를 삽입. 변경이 있으면 True 반환."""
    lines = path.read_text(encoding='utf-8').splitlines(keepends=True)
    out = []
    changed = False

    # 기술 용어: 파일 내 첫 등장 추적
    term_seen = set()

    i = 0
    while i < len(lines):
        line = lines[i]

        # ── 섹션 헤딩 처리 ──
        level = heading_level(line)
        if level >= 3:
            out.append(line)
            raw_term = re.sub(r'^=+\s*', '', line).rstrip('\n')
            term = clean_heading(raw_term)

            if term and len(term) > 1:
                # 다음 줄이 이미 indexterm이 아니면 삽입
                next_line = lines[i + 1] if i + 1 < len(lines) else ''
                if not INDEXTERM_RE.search(next_line) and not next_line.startswith('='):
                    out.append(f'((({term})))\n')
                    changed = True
            i += 1
            continue

        # ── 기술 용어 인라인 마커 처리 ──
        if not INDEXTERM_RE.search(line):
            for pattern, primary, secondary in TECH_TERMS:
                if primary not in term_seen and re.search(pattern, line):
                    # 줄 앞에 indexterm 삽입
                    marker = f'indexterm:[{primary},{secondary}]\n'
                    out.append(marker)
                    term_seen.add(primary)
                    changed = True
                    break  # 줄당 하나의 마커만

        out.append(line)
        i += 1

    if changed:
        path.write_text(''.join(out), encoding='utf-8')
    return changed


def main():
    book_dir = Path(__file__).parent / 'book'
    if not book_dir.exists():
        print(f'book 디렉토리를 찾을 수 없습니다: {book_dir}', file=sys.stderr)
        sys.exit(1)

    # 구조 파일 제외, 콘텐츠 파일만 처리
    exclude = {'index.asc', 'contents.asc', 'appendix.asc', 'index-terms.asc'}
    asc_files = sorted(
        f for f in book_dir.rglob('*.asc')
        if f.name not in exclude
        and not f.name.endswith('-begin.asc')
        and 'index-page' not in f.name
    )

    modified = []
    for f in asc_files:
        if process_file(f):
            modified.append(f.relative_to(book_dir))

    print(f'처리 완료: {len(asc_files)}개 파일 중 {len(modified)}개 수정')
    for p in modified:
        print(f'  ✓ {p}')


if __name__ == '__main__':
    main()
