require 'irb/completion'                                                 
require 'hirb' ; Hirb.enable                                             

ARGV.concat ["--readline", "--prompt-mode", "simple"]                    
IRB.conf[:SAVE_HISTORY] = 10000
IRB.conf[:HISTORY_FILE] = "#{ENV['HOME']}/.irb_history"                  

ActiveRecord::Base.logger.level = 1 # Avoid log in Rails console      
ActiveRecord::Base.logger = Logger.new STDOUT #顯示 SQL statements

ActiveRecord::Base.connection.tables
    def drop_tbl (tblname)
        ActiveRecord::Migration.drop_table(eval(":"+tblname))
    end
    def show_tbls
        tbls = ActiveRecord::Base.connection.tables
        tbls.each { |tbl|
            puts "#{tbl} #{tbl_name(tbl)}"
        }
    end
    def tbl_name(name)
        name.singularize.humanize.split().map{|x| x.capitalize}.join()
    end


    def cols (tblname)
        cols = eval("#{tblname}.column_names")
        ap(cols)
    end
