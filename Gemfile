# GitHub Pages builds this site with the `github-pages` gem, which pins Jekyll
# and every plugin named in _config.yml to the versions Pages actually runs.
# Using the same gem locally and in CI is what makes a preview trustworthy:
# it removes the "rendered fine on my machine, broke on Pages" class of bug.
#
#   bundle install
#   bundle exec jekyll serve      # http://localhost:4000/dulss-study-group/
source "https://rubygems.org"

gem "github-pages", group: :jekyll_plugins

# Timezone data for platforms whose Ruby does not ship it. Harmless elsewhere.
gem "tzinfo-data", platforms: [:mingw, :mswin, :x64_mingw, :jruby]
