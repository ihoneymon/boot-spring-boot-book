부트 스프링 부트 `Boot Spring Boot`
====================

* 작성자: 허니몬 <ihoneymon@gmail.com>

> 스프링 부트 `Spring Boot` 를 기반으로 하는 개발가이드

예제 코드는 [boot-spring-boot](https://github.com/ihoneymon/boot-spring-boot) 저장소를 함께 참고하세요.

> **유지보수 정책**: 새 Spring Boot 버전 출시 시 작업 절차는
> [boot-spring-boot/docs/MAINTENANCE.md](https://github.com/ihoneymon/boot-spring-boot/blob/upgrade/spring-boot-4x/docs/MAINTENANCE.md)를 참고하세요.

## 버전별 신기능 체크아웃 가이드

각 버전 태그를 체크아웃하면 해당 버전 시점의 책 내용을 확인할 수 있습니다.
예제 코드([boot-spring-boot](https://github.com/ihoneymon/boot-spring-boot))와 동일한 태그로 맞추면 코드와 본문을 함께 볼 수 있습니다.

### 저장소 클론

```bash
$ git clone https://github.com/ihoneymon/boot-spring-boot-book.git
$ cd boot-spring-boot-book
$ git checkout upgrade/spring-boot-4x   # 전체 업그레이드 히스토리 브랜치
```

### 버전별 태그 목록 확인

```bash
$ git tag | sort -V
```

### 버전별 체크아웃

```bash
$ git checkout v2.4.13   # Spring Boot 2.4: ApplicationStartup, config.import, Profile Groups
$ git checkout v2.5.14   # Spring Boot 2.5: spring.sql.init.* 통합
$ git checkout v2.6.14   # Spring Boot 2.6: Kubernetes Probes, PathPatternParser
$ git checkout v2.7.18   # Spring Boot 2.7: AutoConfiguration.imports
$ git checkout v3.0.13   # Spring Boot 3.0: Jakarta EE 9, @HttpExchange, Problem Details
$ git checkout v3.1.12   # Spring Boot 3.1: Docker Compose, SSL Bundle, @ServiceConnection
$ git checkout v3.2.12   # Spring Boot 3.2: RestClient, JdbcClient, Virtual Threads
$ git checkout v3.3.13   # Spring Boot 3.3: Structured Logging(JSON), CDS
$ git checkout v3.4.13   # Spring Boot 3.4: MockMvcTester, OTLP 개선
$ git checkout v4.0.6    # Spring Boot 4.0: Spring Framework 7, RestTemplateBuilder 제거
```

### 버전 간 변경 내용 비교

```bash
# 두 버전 사이의 전체 변경사항 확인
$ git diff v2.7.18 v3.0.13

# 특정 챕터 파일만 비교
$ git diff v2.7.18 v3.0.13 -- book/chap03/

# 버전별 커밋 로그 확인
$ git log v2.7.18..v3.0.13 --oneline
```

### 버전별 신기능 요약

| 버전 | 주요 신기능 | 관련 챕터 |
|------|-----------|----------|
| 2.4.13 | ApplicationStartup, spring.config.import, Profile Groups | chap03/03-01, 03-02, 03-03 |
| 2.5.14 | spring.sql.init.* 통합 (spring.datasource.* deprecated) | chap03/03-07 |
| 2.6.14 | Kubernetes Probes, PathPatternParser 기본 전환, 순환 의존성 금지 | chap04/04-01 |
| 2.7.18 | AutoConfiguration.imports, @AutoConfiguration 어노테이션 | chap03/03-15 |
| 3.0.13 | Jakarta EE 9 전환(javax→jakarta), @HttpExchange, Problem Details | chap03/03-11 |
| 3.1.12 | Docker Compose 연동, SSL Bundle, @ServiceConnection | chap03/03-13 |
| 3.2.12 | RestClient, JdbcClient, Virtual Threads(Project Loom) | chap03/03-10 |
| 3.3.13 | Structured Logging(JSON/ECS), CDS, @Fallback | chap03/03-04 |
| 3.4.13 | MockMvcTester(AssertJ 통합), OTLP 트레이싱 개선 | chap03/03-13 |
| 4.0.6 | Spring Framework 7, RestTemplateBuilder 자동구성 제거 | chap03/03-10 |

> **Tip:** 예제 코드 저장소([boot-spring-boot](https://github.com/ihoneymon/boot-spring-boot))에서 동일한 태그로 체크아웃하면,
> 각 버전의 신기능 예제 파일(`src/main/java/.../feature/v{버전}/`)과 책 본문을 함께 확인할 수 있습니다.

---

## 문서생성을 위한 사전요구사항
* [rbenv](https://github.com/rbenv/rbenv) 로 Ruby 3.3.7 설치
* [bundler](http://bundler.io/) 설치

```
$ rbenv install 3.3.7
$ gem install bundler
```

## 문서빌드
```
$ bundle install
$ ./build.sh
```
