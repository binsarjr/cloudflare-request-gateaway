from sanic import Sanic, response
from sanic.request import Request
import cloudscraper
import json

app = Sanic("scraper_api")


@app.route("/", methods=["GET"])
async def scrape(request: Request):
    # Mendapatkan URL target dari query parameter
    target_url = request.args.get("___url")

    if not target_url:
        return response.text("Parameter '___url' harus disediakan", status=400)

    # Mendapatkan headers dari parameter ___headers
    headers_param = request.args.get("___headers")

    if headers_param:
        try:
            headers = json.loads(headers_param)
        except json.JSONDecodeError:
            return response.text(
                "Format JSON pada parameter '___headers' tidak valid", status=400
            )
    else:
        headers = {}

    # Mendapatkan cookies dari parameter ___cookies
    cookies_param = request.args.get("___cookies")

    if cookies_param:
        try:
            cookies = json.loads(cookies_param)
        except json.JSONDecodeError:
            return response.text(
                "Format JSON pada parameter '___cookies' tidak valid", status=400
            )
    else:
        cookies = {}

    # Membuat objek cloudscraper
    scraper = cloudscraper.create_scraper()

    try:
        # Melakukan request GET ke URL target
        scraped_response = scraper.get(target_url, headers=headers, cookies=cookies)

        # Menyiapkan response Sanic
        sanic_response = response.raw(
            body=scraped_response.content,
            status=scraped_response.status_code,
        )

        # Meneruskan headers dari respons asli ke respons Sanic
        for header_key, header_value in scraped_response.headers.items():
            sanic_response.headers[header_key] = header_value

        return sanic_response

    except Exception as e:
        return response.text(f"Error: {str(e)}", status=500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
