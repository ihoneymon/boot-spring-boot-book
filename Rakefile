namespace :book do
  desc 'prepare build'
  task :prebuild do
    Dir.mkdir 'images' unless Dir.exists? 'images'
    Dir.glob("book/*/images/*").each do |image|
      FileUtils.copy(image, "images/" + File.basename(image))
    end
  end

  desc 'build basic book formats'
  task :build => :prebuild do
    puts "Converting to HTML..."
    `bundle exec asciidoctor boot-spring-boot.asc`
    puts " -- HTML output at boot-spring-boot.html"

    puts "Converting to PDF... (this one takes a while)"
    `bundle exec asciidoctor-pdf -r asciidoctor-pdf-cjk-kai_gen_gothic -a pdf-style=KaiGenGothicKR boot-spring-boot.asc -o boot-spring-boot.pdf`
    puts " -- PDF  output at boot-spring-boot.pdf"
  end
end

task :default => "book:build"
