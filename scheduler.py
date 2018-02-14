from crontab import CronTab
import configparser

config = configparser.ConfigParser()
config.read('configuration.txt')
user = config['crontab']['User']
script = config['crontab']['Script']

cron = CronTab(user)
job = cron.new(command='python %s' % script)
job.hour.every(2)
cron.write()
