require 'irb/completion'                                                 
require 'hirb' ; Hirb.enable                                             

ARGV.concat ["--readline", "--prompt-mode", "simple"]                    
IRB.conf[:SAVE_HISTORY] = 1000                                           
IRB.conf[:HISTORY_FILE] = "#{ENV['HOME']}/.irb_history"                  

ActiveRecord::Base.logger.level = 1 # Avoid log in Rails console         
ActiveRecord::Base.connection.tables
    def drop_tbl (tblname)
        ActiveRecord::Migration.drop_table(eval(":"+tblname))
    end
    def show_tbls
        tbls = ActiveRecord::Base.connection.tables
        tbls.each { |tbl|
            puts "#{tbl} #{tbl.singularize.humanize}"
        }
    end
