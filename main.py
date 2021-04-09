import requests as req
from bs4 import BeautifulSoup
from env import ACCEPT_LNG,USER_AGENT, my_email,password,address
import smtplib


def get_inputs():
    target_url = input("Please input the url of the product you want to track.\n")
    try:
        target_price = float(input("Please input the target price for sending alert.\n"))
    except ValueError:
        print("Invalid input, price should be a number or float.")
        get_inputs()
    else:
        scraped_data = get_scarping_data(target_url)
        send_alert = check_price(scraped_data[0],target_price)
        if send_alert:
            send_mail(scraped_data[1],scraped_data[0],target_url)


def get_scarping_data(url):
    headers = {
        'Accept-Language':ACCEPT_LNG,
        'User-Agent': USER_AGENT
    }

    res = req.get(url=url,headers = headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"html.parser")
    price = float(soup.find(name="span",class_="priceBlockBuyingPriceString").getText()[1:])
    title = (soup.find(name="span",class_="product-title-word-break").getText()[8:-7])
    return (price,title)


def check_price(pprice,tprice):
    return pprice <= tprice

def send_mail(title,pprice,url):
    title = title.encode('utf-8')
    print(type(title))
    letter = f"\nHey there!!!\nA product you set price alert for has reached your expected price.\nThe product is {title}\nPresent price: ${pprice}\nLink: {url}\n\nHope you enjoyed our alert service.\nThank you and enjoy shopping."
    with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
        connection.starttls()
        connection.login(user=my_email,password=password)
        connection.sendmail(to_addrs=address, from_addr=my_email,msg=f"Subject: Amazon Price Alert!!!\n\n{letter}")
    print("Email alert sent")




get_inputs()