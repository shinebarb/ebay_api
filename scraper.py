from lxml import html
import validators
import requests

headers = {
    'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }


#Enter your proxy url here
proxy_url = "https://ebay.shinealom.workers.dev"

def create_url(wallmart_url):

    try:

        clean_url = wallmart_url.replace("https://ebay.com", proxy_url).replace("https://www.ebay.com", proxy_url)
        return clean_url

    except: 
        return {
            'status' : 'error'
        }

        


def fetch_website_content(url):
    try:

        response = requests.get(url, headers=headers)
        print(response.status_code)
        # print("wor")

        
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(response.text)
            print("HTML content saved to page.html")

        if response.status_code == 200:
            html_content = response.text
            return html_content
        
        else:
            return {
            'message' : 'Error while fetching website!',
            'status' : 'error'
        }
        

    except Exception as e:
        return {
            'message' : 'An error occured while fetching website!',
            'status' : 'error',
            'exception' : e
        }





def product_details(url):

    try:
        proxy_url = create_url(url)
        

        html_content = fetch_website_content(proxy_url)
        # print(html_content)

        doc = html.fromstring(html_content)
        
         

        # Try to check if xpath have any element
        if doc.xpath("//h1/span"):
            # If it has then it will set it's value
            title = doc.xpath("//h1/span/text()")[0]
        else:
            #If not then it will set the value as Null
            title = 'Null'
        
       


        # Price xpath 
        if doc.xpath("//div[@class='x-price-primary']/span"):
            price = doc.xpath("//div[@class='x-price-primary']/span/text()")[0]
            price = str(price).replace("US", "").replace(" ", "").replace("$", "")
        else:
            price = "Null"


        # Seller 
        if doc.xpath("//div[@class='ux-seller-section__item--seller']/a[1]/span"):
            seller = doc.xpath("//div[@class='ux-seller-section__item--seller']/a[1]/span/text()")[0]
        else:
            seller = "Ebay Seller"


        
        # # Rating 
        # if doc.xpath("//span[@class='f7 rating-number']"):
        #     rating = doc.xpath("//span[@class='f7 rating-number']/text()")[0]
        #     rating = str(rating).replace("(", "").replace(")", "")
        #     print("hello")
            
        # else:
        #     rating = "No Ratings"

      


        # Image link
        if doc.xpath("(//div[@class='ux-image-magnify__container'])[1]/img"):
            image_link = doc.xpath("(//div[@class='ux-image-magnify__container'])[1]/img/@src")[0]

            if image_link == "https://i.ebayimg.com/images/g/krYAAOSwq6Zj0dta/s-l500.jpg":
                image_link = "https://i.ebayimg.com/images/g/krYAAOSwq6Zj0dta/s-l1600.jpg"
            
        else:
            image_link = "Null"

        return {
            'title' : title,
            'price' : price,
            'seller' : seller,
            # 'rating' : rating,
            'image_link' : image_link,
            'url' : url,
            'status' : 'success'
        }

    
    except Exception as e:
        {
            'message' : 'An error occured while extracting product details!',
            'status' : 'error',
            'exception' : e
        }


product_details("https://www.ebay.com/itm/334657205399?hash=item4deb1fb497:g:krYAAOSwq6Zj0dta&_trksid=p5731.m3795")