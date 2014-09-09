import os, studioLibrary

def go():
	library_path = os.path.join(os.environ['PRODUCTION_DIR'],"studio_library")
	studioLibrary.main(root=library_path)

if __name__ == '__main__':
	go()
