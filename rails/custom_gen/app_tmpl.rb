app_name=@app_name 
remove_file "README.rdoc"
create_file "README.md", "TODO"

#install gemfile
# Gems used only for assets and not required   
# # in production environments by default.       
gem 'coffee-rails', '~> 3.2.1' , group: "assets"              
gem 'bootstrap-sass', '~> 2.3.2.0', group: "assets"                  
gem 'haml' # let html like (scss for css)
gem 'hirb-unicode'
gem 'devise'
gem 'will_paginate', '~> 3.0'
gem 'nokogiri' , '1.6.0'
gem 'rspec'
gem 'cancan'
gem 'carrierwave' # File Upload
gem 'awesome_print', :require => 'ap'
gem 'quiet_assets', :group => :development #https://github.com/evrone/quiet_assets
gem 'faker' ,:group => :development
gem "faker-isbn", "~> 0.0.4" , :group => :development
gem 'tinymce-rails'


#run "bundle install"
#if yes? "Wanna to gen a root controller? [yes/no]"
#name = ask("scaffold name called?").underscore
#cols = ask("input cols you want").underscore
#end

name="book"
cols="name:string isbn:integer price:integer comment:text"
generate :scaffold, "#{name}  #{cols}"
route "root :to=> '#{name.pluralize}\#index'"
remove_file "public/index.html"


#if yes?("Would you like to install Devise? [yes/no]")
    gem "devise"
    generate "devise:install"
    #model_name = ask("What would you like the user model to be called? [user]")
    model_name = "user" 
    generate "devise", model_name
    generate "devise:views"





    gsub_file 'config/environments/development.rb', /config.action_mailer.raise_delivery_errors = false/ do
        <<-RUBY
            config.action_mailer.default_url_options = { :host => "localhost:3000" }
            # A dummy setup for development - no deliveries, but logged
                        
            config.action_mailer.delivery_method = :smtp
            config.action_mailer.raise_delivery_errors = true
            config.action_mailer.default :charset => "utf-8"

            config.action_mailer.smtp_settings = {
            :address => "smtp.gmail.com",  
            :port => 587,
            :domain => "gmail.com",  
            :authentication => :plain,
            :user_name => ENV['gmail_user'],
            :password => ENV['gmail_passwd'] ,
            :enable_starttls_auto => true
            }  
        RUBY
    end

    gsub_file 'config/initializers/devise.rb', /config.password_length = 8..128/ do
        <<-RUBY
                config.password_length = 1..128
        RUBY
    end
    #tinymce
   
    inject_into_file 'app/assets/javascripts/application.js', :after => "//= require jquery_ujs\n" do
        <<-RUBY
           //= require tinymce-jquery 
        RUBY
    end 



    #add confirmable
    confirm_cols='confirmation_token:string:index:unique confirmed_at:datetime confirmation_sent_at:datetime'
    run "rails g migration add_confirmable_to_user #{confirm_cols}" 


    #CanCan #http://zool.iteye.com/blog/713438
    inject_into_file 'app/models/user.rb', :after => "ActiveRecord::Base\n" do
        <<-RUBY
        ROLES = %w[admin manager staff banned] 
        
        RUBY
    end 
    inject_into_file 'app/models/user.rb', :after => /^\s+attr_accessible.*/ do
        <<-RUBY
,:role
        RUBY
    end
    run 'rails g migration add_role_to_users role:string '

    run 'rails generate mailer UserMailer confirm'
    #replace default mailer function
    inject_into_file 'app/mailers/user_mailer.rb', :after => "def confirm\n" do        
        <<-RUBY
    end
    def confirm(email)
    @message = "Thank you for confirmation!"
    mail(:to => email, :subject => "Registered")  
    return
        RUBY
    end


#end

#setting template


def tmpl_name(name)
    orig_file="../tmpl/#{name}"
    if name.include? "helper.rb"
        return "#{orig_file} app/helpers/#{name}" 
    end
    if name.include? "html.erb"
        return "#{orig_file} app/views/layouts/#{name}" 
    end
    if name.include? "css.scss"
        return "#{orig_file} app/assets/stylesheets/#{name}" 
    end
end
#setting template

#get all template files
files = `ls ../tmpl`
files.split().each{|f|
    run 'cp '+tmpl_name(f)
}


def dest_dir(fname)
    puts fname
    dir=fname.split('.')[0..-3].join('/')
    f=fname.split('.')[-2..3].join('.')
    return dir+'/'+f
end
#CanCan
dir='../custom_files/'
lists = `ls #{dir}`
lists.split().each{|f|
    run 'cp '+ dir+f+' '+dest_dir(f)
}

# for application.yml refer to https://github.com/railscasts/085-yaml-configuration-revised/blob/master/blog-after/config/application.rb
gsub_file 'config/application.rb', /if defined\?\(Bundler\)/ 
do

<<-RUBY

#setting load secret variables
config = YAML.load(File.read(File.expand_path('../application.yml', __FILE__)))
config.merge! config.fetch(Rails.env, {})
config.each do |key, value|
  ENV[key] = value unless value.kind_of? Hash
end

if defined?(Bundler)

RUBY

end



#finish
rake "db:migrate"
rake "routes"

#github commit
git :init
run "cp ~/common_lib/rails/.gitignore ./"
git add: "."
git commit: %Q{ -m 'Initial commit' }
