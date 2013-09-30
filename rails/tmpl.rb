#template.rb


#install gemfile
# Gems used only for assets and not required   
# # in production environments by default.       
group :assets do                               
    gem 'sass-rails',   '~> 3.2.3'               
    gem 'coffee-rails', '~> 3.2.1'               
    gem 'bootstrap-sass', '~> 2.3.2.0'                  
end
    gem 'hirb-unicode'
    gem 'devise'
    gem 'will_paginate', '~> 3.0'
    gem 'nokogiri' , '1.6.0'
    gem 'rspec'
    gem 'cancan'
    gem 'carrierwave' # File Upload
    gem 'awesome_print', :require => 'ap'
    gem 'quiet_assets', :group => :development #https://github.com/evrone/quiet_assets

    run "rspec --init"
    run "rm public/index.html"

    git :init
    run "cp ~/common_lib/rails/.gitignore ./"
    git add: "."
    git commit: %Q{ -m 'Initial commit' }


