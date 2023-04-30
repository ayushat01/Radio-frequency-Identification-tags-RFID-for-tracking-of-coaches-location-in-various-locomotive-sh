import struct
import socket
import sys
import threading
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# --- constants ---

HOST = '192.168.1.100'
print("ayush")

PORT = 10009

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db=firestore.client()



def handle_client(conn, addr):


    try:
        while True:
            vl = conn.recv(128)

            vl = str(vl)
            print(vl)
            spl_word1='readsn='
            spl_word2 = 'id='

            res1 = vl.split(spl_word1, 1)
            res2 = vl.split(spl_word2, 1)
            splitString1 = res1[1]
            splitString2 = res2[1]
            s_n0=splitString1[0:13]
            id=splitString2[0:4]


            # print(s_n0)
            # print(id)   # datu=str(data)
            data = {'Id': id, 'ReaderSerialNo':s_n0,'in_time':'NA'  , 'out_time':'NA','shopId':'shellShop','status  ':'in' }
            # db.collection('ShopTagStatus').add(data)
			#we got the serial_number of reader and tag_id here 
			#check from db for reader using serial_number, you will get associated shop_id, reader_type(entry or exit) from this
			#check for tag_id from db
			#if db query match
			  #db entry is detected i.e tag was detected earlier by reader,
			  #if detected tag from same reader 
			    #same reader detected the tag it could be a false entry 
				#if timestamp of this entry is less than 15 mins'
				  #ignore this entry, by marking it reentry 
				#else
				  #this could be exit from same reader 
			  #else
			    #other enrty reader can only detect exist but it should be from same shop
                #if it is exit reader from same shop
				   #update db for this tag, by setting time, staus as out, shop name etc.
                #else		
                   #this case is not possible we can update another fault table: tbd 				   
			#else
			   #if this is from entry 
			     #this is case for first time detection, update databse for tag_id, time, staus as in 
			   #else
			     #invalid situation, not allowed. we can update another fault table for this kind of entry.
				 
            db.collection('ShopTagStatus').document(id).set(data)
            time.sleep(2)
            # print(datu[6:10])



    except BrokenPipeError:
        print()
        # print('[DEBUG] addr:', addr, 'Connection closed by client?')
    except Exception as ex:
        print()
        # print('[DEBUG] addr:', addr, 'Exception:', ex, )
    finally:
        conn.close()



try:
    print()


    # print('[DEBUG] create socket')


    s = socket.socket()




    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)



    # print('[DEBUG] bind:', (HOST, PORT))

    s.bind((HOST, PORT))



    # print('[DEBUG] listen')

    s.listen(1)

    while True:


        # print('[DEBUG] accept ... waiting')

        conn, addr = s.accept()

        # print('[DEBUG] addr:', addr)
        print("Running...")
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()



except Exception as ex:
    print()
    # print(ex)
except KeyboardInterrupt as ex:
    print()
    # print(ex)
except:
    print()
    # print(sys.exc_info())
finally:


    # print('[DEBUG] close socket')

    s.close()


