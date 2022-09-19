import os
import random
import stat
import time

import fuse


class InfinityFolderFilesystem(fuse.LoggingMixIn, fuse.Operations):
	def readdir(self, path, fh):
		if len(path) < 500:
			return ['.', '..'] + [hash(random.randint(0, 2 ** (4 * 8))).to_bytes(4, byteorder='big').hex() for i in range(100)]
		return ['.', '..', 'hehe']

	def getattr(self, path, fh=None):
		return {
			'st_mode': 0o774 | stat.S_IFDIR,
			'st_nlink': 1,
			'st_uid': os.getuid(),
			'st_gid': os.getgid(),
			'st_ctime': time.time(),
			'st_mtime': time.time(),
			'st_actime': time.time()
		}


if __name__ == "__main__":
	mount_point = input("Enter mount point : ")
	if os.path.isdir(mount_point) and len(os.listdir(mount_point)) == 0:
		fuse.FUSE(InfinityFolderFilesystem(), mount_point, foreground=True)
	else:
		print("Error : specified mount point does not exist or is not empty")
