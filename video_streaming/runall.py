import thread 
import app

try:
 thread.start_new_thread( index(), ("Thread-1", 2, ) )
 thread.start_new_thread( gen(camera), ("Thread-2", 2, ) )
 thread.start_new_thread( video_feed(), ("Thread-2", 2, ) )
except:
   print "Error: unable to start thread"
   
pass



