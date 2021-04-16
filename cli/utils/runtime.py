# Not so interesting utils to check on total execution time
from datetime import datetime

start_time: None
end_time: None

def start_counter(callback):
	start_time = datetime.now()

	callback()

	end_time = datetime.now()
	print('Total Execution Duration: {}'.format(end_time - start_time))

# def end_counter():
# 	print(start_time)
# 	end_time = datetime.now()
# 	print('Total Execution Duration: {}'.format(end_time - start_time))
