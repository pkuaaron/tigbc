from selenium import webdriver
import time
import pandas as pd

# f=open('/home/min/tigbc/tigbc/download.html')
# lines=f.readlines()
# img_link=[l[l.index('id=')+4:l.index('" class')] for l in lines[:-3] if l.count('class="overlay-image" src="http://cf.c.ooyala.com')>0]
#
# f1=open('/home/min/tigbc/tigbc/download1.html','w')
# f1.write('\n'.join(img_link))
# f1.close()
#
# import pdb; pdb.set_trace()
driver = webdriver.Chrome()

driver.get("https://www.oaclub.org/club#episodes")
#Login to the website
driver.find_elements_by_name('user')[0].send_keys('pkuaaron@gmail.com')
driver.find_elements_by_name('password')[0].send_keys('59kgbmtx')
driver.find_element_by_class_name('btn-greenInner').click()
time.sleep(10.0)


driver.get("https://www.oaclub.org/club#episodes")
time.sleep(10.0)
f=open('/home/min/tigbc/tigbc/download1.html')
images=f.readlines()

album=[]
titles=[]
sources=[]

failed_album=[]


for img in images:
    img=img.strip()
    print(img)
    image_idx=img[:-6]
    # import pdb; pdb.set_trace()
    try:
        album_image = driver.find_elements_by_id(img)
        time.sleep(1.0)
        webdriver.ActionChains(driver).move_to_element(album_image[0] ).click(album_image[0] ).perform()
        time.sleep(2.0)
    except Exception as e:
        failed_album.append(img)
        continue

    for i in range(1,30):
        try:
            print("{}-{}".format(image_idx,i))
            a_link=driver.find_element_by_xpath('//a[@data-episode-id="{}-{}"]'.format(image_idx,i))
            webdriver.ActionChains(driver).move_to_element(a_link ).click(a_link ).perform()
            # a_link.click()
            time.sleep(4.0)
            link=driver.find_element_by_class_name('track-content')
            html=link.get_attribute('innerHTML')
            title_start=html.index('class="track-title"')
            title_end=html.index('class="track-description"')
            title=html[title_start:title_end]

            start_scr=html.index('<source src="http://cf.c.ooyala.com/')
            end_scr=html.index('.m4a')
            scr=html[start_scr:end_scr+4]
            album.append(img)
            titles.append(title)
            sources.append(scr)
        except Exception as e:
            break
            time.sleep(5.0)
# import pdb; pdb.set_trace()
df=pd.DataFrame.from_dict({'Album':album,'Title':titles,'Source':sources})
df.to_csv('/home/min/tigbc/tigbc/aio_album1.csv',index=False)
df1=pd.DataFrame.from_dict({'FailedAlbum':failed_album})
df1.to_csv('/home/min/tigbc/tigbc/failed_album1.csv',index=False)



# /html/body/div[2]/div[3]/div/div[2]/div[2]/div[27]/div[2]/div/ol[1]/li[1]/a
