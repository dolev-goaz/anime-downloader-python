from urllib import request

def downloadProgress(filename, percentage):
        print(f'{filename}: {percentage}%')
        
def downloadFinish(filename):
        print(f'{filename} has finished downloading!')

class Downloader:
	def __init__(self, href, filename, full_path, update_hook=downloadProgress, finish_hook=downloadFinish):
		self.href = href
		self.filename = filename
		self.full_path = full_path
		self.percentage = 0
		self.update_hook = update_hook
		self.finish_hook = finish_hook
	
	def start(self):
                print('Downloading ' + self.filename)
                request.urlretrieve(self.href, self.full_path, reporthook=self.downloadMiddleware)
		
	def downloadMiddleware(self, count, blockSize, totalSize):
		percentage = int(count * blockSize * 100 / totalSize) 
		if self.percentage != percentage:
			self.percentage = percentage
			if self.update_hook:
				self.update_hook(self.filename, self.percentage)


			if self.percentage == 100 and self.finish_hook:
				self.finish_hook(self.filename)

	
		

