import json

import requests

from helpers.envs.amazon_envs import AmazonEnvs
from parsers.amazon.parseAmazonProduct import ParseAmazonProduct


class AmazonRainForestAPI:
    def __init__(self, product, domain):
        self.asin = product
        self.domain = domain

    def __make_request(self):
        response = requests.get(AmazonEnvs.AMAZON_RAINFOREST_BASE_URL.value,
                                self.__get_params(product=self.asin, domain=self.domain))
        if response:
            return response.json()

    @staticmethod
    def __get_params(product, domain=None):
        api_domain = AmazonEnvs.AMAZON_RAINFOREST_BASE_DOMAIN.value if not domain else domain
        return {
            'api_key': AmazonEnvs.AMAZON_RAINFOREST_API.value,
            'amazon_domain': api_domain,
            'asin': product,
            'type': 'product'

        }

    def get_product_full_info(self):
        json_response = self.__make_request()
        # json_response = self.test_json()

        parser = ParseAmazonProduct(json_response)
        return parser.parse_full_data()

    # Temporary data
    def test_json(self):
        return {
            "demo_message": "* Demo results are truncated for brevity *",
            "request_parameters": {
                "amazon_domain": "amazon.com",
                "type": "product",
                "asin": "B073JYC4XM"
            },
            "request_metadata": {
                "amazon_url": "https://www.amazon.com/dp/B073JYC4XM?th=1&psc=1"
            },
            "product": {
                "title": "SanDisk 128GB Ultra MicroSDXC UHS-I Memory Card with Adapter - 100MB/s, C10, U1, Full HD, A1, Micro SD Card - SDSQUAR-128G-GN6MA",
                "search_alias": {
                    "title": "Electronics",
                    "value": "electronics"
                },
                "keywords": "SanDisk,128GB,Ultra,MicroSDXC,UHS-I,Memory,Card,with,Adapter,-,100MB/s,,C10,,U1,,Full,HD,,A1,,Micro,SD,Card,-,SDSQUAR-128G-GN6MA",
                "keywords_list": [
                    "SanDisk",
                    "128GB",
                    "Ultra",
                    "MicroSDXC",
                    "UHS-I",
                    "Memory",
                    "Card",
                    "with",
                    "Adapter",
                    "100MB/s",
                    "Full",
                    "Micro",
                    "Card",
                    "SDSQUAR-128G-GN6MA"
                ],
                "asin": "B073JYC4XM",
                "link": "https://www.amazon.com/SanDisk-128GB-microSDXC-Memory-Adapter/dp/B073JYC4XM",
                "brand": "SanDisk",
                "protection_plans": [
                    {
                        "asin": "B00VF4JT6G",
                        "title": "2-year Photo and Data Recovery Plan",
                        "price": {
                            "symbol": "$",
                            "value": 2.99,
                            "currency": "USD",
                            "raw": "$2.99"
                        }
                    },
                    {
                        "asin": "B011WVM2B0",
                        "title": "3-year Photo and Data Recovery Plan",
                        "price": {
                            "symbol": "$",
                            "value": 3.99,
                            "currency": "USD",
                            "raw": "$3.99"
                        }
                    }
                ],
                "sell_on_amazon": True,
                "documents": [
                    {
                        "name": "Specification Sheet (PDF)",
                        "link": "https://m.media-amazon.com/images/I/91NqBqLsumS.pdf"
                    }
                ],
                "categories": [
                    {
                        "name": "Electronics",
                        "link": "https://www.amazon.com/electronics-store/b/ref=dp_bc_aui_C_1?ie=UTF8&node=172282",
                        "category_id": "172282"
                    },
                    {
                        "name": "Computers & Accessories",
                        "link": "https://www.amazon.com/computer-pc-hardware-accessories-add-ons/b/ref=dp_bc_aui_C_2?ie=UTF8&node=541966",
                        "category_id": "541966"
                    },
                    {
                        "name": "Computer Accessories & Peripherals",
                        "link": "https://www.amazon.com/Computer-Accessories-Supplies/b/ref=dp_bc_aui_C_3?ie=UTF8&node=172456",
                        "category_id": "172456"
                    },
                    {
                        "name": "Memory Cards",
                        "link": "https://www.amazon.com/Memory-Cards-Computer-Add-Ons-Computers/b/ref=dp_bc_aui_C_4?ie=UTF8&node=516866",
                        "category_id": "516866"
                    },
                    {
                        "name": "Micro SD Cards",
                        "link": "https://www.amazon.com/Micro-SD-Memory-Cards/b/ref=dp_bc_aui_C_5?ie=UTF8&node=3015433011",
                        "category_id": "3015433011"
                    }
                ],
                "categories_flat": "Electronics > Computers & Accessories > Computer Accessories & Peripherals > Memory Cards > Micro SD Cards",
                "description": "SanDisk Ultra microSDXC and microSDHC cards are fast for better pictures, app performance, and Full HD video. Ideal for Android smartphones and tablets, these A1-rated cards load apps faster for a better smartphone experience. Available in capacities up to 400GB, you have the capacity to take more pictures and Full HD video and capture life at its fullest. Built to perform in harsh conditions, SanDisk Ultra microSD cards are waterproof, temperature proof, shockproof, and X-ray proof. 1GB=1,000,000,000 bytes. Actual user storage less. (For 64GB-256GB): Up to 100MB/s read speed; write speed lower. (For 16GB-32GB): Up to 98MB/s read speed; write speed lower. Based on internal testing; performance may be lower depending on host device, interface, usage conditions and other factors. 1MB=1,000,000 bytes. (1) Full HD (1920x1080) video support may vary based upon host device, file attributes, and other factors. (2) Card only. (3) Results may vary based on host device, app type and other factors. (4) Download and installation required. (5) Based on 4.1GB transfer of photos (Average file 3.5MB) with USB 3.0 reader. Results may vary based on host device, file attributes and other factors. 6) Approximations; Results and Full HD (1920x1080) video support may vary based on host device, file attributes and other factors.",
                "a_plus_content": {
                    "has_a_plus_content": True,
                    "has_brand_story": False,
                    "third_party": False
                },
                "sub_title": {
                    "text": "Visit the SanDisk Store",
                    "link": "https://www.amazon.com/stores/SanDisk/page/CD971F4B-EE23-4EA1-96E3-567678AC9C0A?ref_=ast_bln"
                },
                "amazons_choice": {
                    "keywords": "in Micro SD Memory Cards by SanDisk"
                },
                "rating": 4.7,
                "rating_breakdown": {
                    "five_star": {
                        "percentage": 84,
                        "count": 181617
                    },
                    "four_star": {
                        "percentage": 10,
                        "count": 21621
                    },
                    "three_star": {
                        "percentage": 3,
                        "count": 6486
                    },
                    "two_star": {
                        "percentage": 1,
                        "count": 2162
                    },
                    "one_star": {
                        "percentage": 2,
                        "count": 4324
                    }
                },
                "ratings_total": 216211,
                "main_image": {
                    "link": "https://m.media-amazon.com/images/I/617NtexaW2L.jpg"
                },
                "images": [
                    {
                        "link": "https://m.media-amazon.com/images/I/617NtexaW2L._AC_SL1500_.jpg",
                        "variant": "MAIN"
                    },
                    {
                        "link": "https://m.media-amazon.com/images/I/71cs-unZZqL._AC_SL1500_.jpg",
                        "variant": "PT01"
                    },
                    {
                        "link": "https://m.media-amazon.com/images/I/61P3Jhyw2DL._AC_SL1000_.jpg",
                        "variant": "PT02"
                    },
                    {
                        "link": "https://m.media-amazon.com/images/I/61Cu4fF1MBL._AC_SL1000_.jpg",
                        "variant": "PT03"
                    },
                    {
                        "link": "https://m.media-amazon.com/images/I/81ffX34OsAL._AC_SL1500_.jpg",
                        "variant": "PT04"
                    },
                    {
                        "link": "https://m.media-amazon.com/images/I/61c0HMo4mhL._AC_SL1500_.jpg",
                        "variant": "PT05"
                    }
                ],
                "images_count": 6,
                "images_flat": "https://m.media-amazon.com/images/I/617NtexaW2L._AC_SL1500_.jpg,https://m.media-amazon.com/images/I/71cs-unZZqL._AC_SL1500_.jpg,https://m.media-amazon.com/images/I/61P3Jhyw2DL._AC_SL1000_.jpg,https://m.media-amazon.com/images/I/61Cu4fF1MBL._AC_SL1000_.jpg,https://m.media-amazon.com/images/I/81ffX34OsAL._AC_SL1500_.jpg,https://m.media-amazon.com/images/I/61c0HMo4mhL._AC_SL1500_.jpg",
                "videos": [
                    {
                        "duration_seconds": 34,
                        "width": 854,
                        "height": 480,
                        "link": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/5c1181fe-7c83-4436-a466-0021e84ef18e/default.jobtemplate.mp4.480.mp4",
                        "thumbnail": "https://m.media-amazon.com/images/I/51hoTKyxlxL.SX522_.jpg",
                        "is_hero_video": False,
                        "variant": "MAIN",
                        "group_id": "IB_G1",
                        "group_type": "videos_for_this_product",
                        "title": "SanDisk Ultra microSD Memory Card"
                    },
                    {
                        "duration_seconds": 109,
                        "width": 854,
                        "height": 480,
                        "link": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/12fbb4ec-2e93-42fa-b1d5-db97febf200d/default.jobtemplate.mp4.480.mp4",
                        "thumbnail": "https://m.media-amazon.com/images/I/B1svx8b87xL.SX522_.png",
                        "is_hero_video": False,
                        "variant": "MAIN",
                        "group_id": "IB_G2",
                        "group_type": "related_videos",
                        "title": "SanDisk Ultra MicroSDXC Card - REVIEW"
                    },
                    {
                        "duration_seconds": 81,
                        "width": 854,
                        "height": 480,
                        "link": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/a425c4c7-541d-4402-aad6-72a832e98d47/default.jobtemplate.mp4.480.mp4",
                        "thumbnail": "https://m.media-amazon.com/images/I/51aTW0KrjgL.SX522_.jpg",
                        "is_hero_video": False,
                        "variant": "MAIN",
                        "group_id": "IB_G2",
                        "group_type": "related_videos",
                        "title": "Will it Work With a Nintendo Switch??"
                    }
                ],
                "videos_count": 3,
                "videos_flat": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/5c1181fe-7c83-4436-a466-0021e84ef18e/default.jobtemplate.mp4.480.mp4,https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/12fbb4ec-2e93-42fa-b1d5-db97febf200d/default.jobtemplate.mp4.480.mp4,https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/a425c4c7-541d-4402-aad6-72a832e98d47/default.jobtemplate.mp4.480.mp4",
                "videos_additional": [
                    {
                        "id": "amzn1.vse.video.765f9cbc6f9c451d9c655c108c68c3b6",
                        "product_asin": "B073JYC4XM",
                        "parent_asin": "B073JYC4XM",
                        "title": "Works fine for my fire 10.....",
                        "profile_image_url": "https://www.amazon.com/avatar/default/amzn1.account.AHEFBJSTUBLB4ACJSQX5PUNBZPVQ?max_width=110&square=True",
                        "profile_link": "/gp/profile/amzn1.account.AHEFBJSTUBLB4ACJSQX5PUNBZPVQ",
                        "public_name": "PD Rubi",
                        "creator_type": "Customer",
                        "vendor_code": "AOD60",
                        "vendor_name": "PD Rubi",
                        "video_image_id": "A1tY5IwAqML",
                        "video_image_url": "https://m.media-amazon.com/images/I/A1tY5IwAqML._CR3,0,1914,1080_SR684,386_.png",
                        "video_image_url_unchanged": "https://images-na.ssl-images-amazon.com/images/I/A1tY5IwAqML.png",
                        "video_image_width": "1920",
                        "video_image_height": "1080",
                        "video_image_extension": "png",
                        "video_url": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/v2/b93c11e1-7255-5570-bbd1-ef26768ddcb3/ShortForm-Generic-480p-16-9-1409173089793-rpcbe5.mp4",
                        "video_previews": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/46d20853-bf07-4944-9f1b-538d54f46d59/videopreview.jobtemplate.mp4.342X192P_20HZ_350KBPS_VER_1_0.mp4,342X192P_20HZ_350KBPS_VER_1_0,video/mp4",
                        "video_mime_type": "video/mp4",
                        "duration": "2:43",
                        "closed_captions": "en,https://m.media-amazon.com/images/S/vse-vms-closed-captions-artifact-us-east-1-prod/closedCaptions/4c1bc796-0cb0-4b59-b758-f83c8edb2ab1.vtt",
                        "type": "videos_for_this_product"
                    },
                    {
                        "id": "amzn1.vse.video.04a2995e89e54b1ba47c781ae5b2f52b",
                        "product_asin": "B073JYC4XM",
                        "parent_asin": "B073JYC4XM",
                        "related_products": "B08GYKNCCP, B08CLNX58K, B08KB38516",
                        "title": "SanDisk Ultra MicroSDXC Card - REVIEW",
                        "profile_image_url": "https://images-na.ssl-images-amazon.com/images/S/influencer-profile-image-prod/logo/evolvingrealest_1605845351956_original._CR0,0,333,333_._FMjpg_.jpeg",
                        "profile_link": "/shop/evolvingrealest",
                        "public_name": "See it. Buy it. Love it!",
                        "creator_type": "Influencer",
                        "vendor_code": "evolvingrealest:shop",
                        "vendor_name": "See it. Buy it. Love it!",
                        "vendor_tracking_id": "kjvilleneuve-20",
                        "video_image_id": "B1svx8b87xL",
                        "video_image_url": "https://m.media-amazon.com/images/I/B1svx8b87xL._CR3,0,1914,1080_SR684,386_.png",
                        "video_image_url_unchanged": "https://m.media-amazon.com/images/I/B1svx8b87xL.png",
                        "video_image_width": "1920",
                        "video_image_height": "1080",
                        "video_image_extension": "png",
                        "video_url": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/12fbb4ec-2e93-42fa-b1d5-db97febf200d/default.jobtemplate.hls.m3u8",
                        "video_previews": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/26722837-852c-407a-a758-d22447285fba/videopreview.jobtemplate.mp4.342X192P_20HZ_350KBPS_VER_1_0.mp4,342X192P_20HZ_350KBPS_VER_1_0,video/mp4",
                        "video_mime_type": "application/x-mpegURL",
                        "duration": "1:49",
                        "closed_captions": "en,https://m.media-amazon.com/images/S/vse-vms-closed-captions-artifact-us-east-1-prod/closedCaptions/75d1ac13-ed83-4013-abbf-ef3a135a5c66.vtt",
                        "type": "videos_for_this_product"
                    },
                    {
                        "id": "amzn1.vse.video.dc8437a03dca4111bf9bb4b629d238f1",
                        "product_asin": "B073JYC4XM",
                        "parent_asin": "B073JYC4XM",
                        "title": "Bought 2 but got one defective",
                        "profile_image_url": "https://www.amazon.com/avatar/default/amzn1.account.AFG7HC3O335W6RLIRQW5RCQXTGUA?max_width=110&square=True",
                        "profile_link": "/gp/profile/amzn1.account.AFG7HC3O335W6RLIRQW5RCQXTGUA",
                        "public_name": "Danilo R.",
                        "creator_type": "Customer",
                        "vendor_code": "AOD60",
                        "vendor_name": "Danilo R.",
                        "video_image_id": "91tYJTabe6L",
                        "video_image_url": "https://m.media-amazon.com/images/I/91tYJTabe6L._CR3,0,1914,1080_SR684,386_.png",
                        "video_image_url_unchanged": "https://images-na.ssl-images-amazon.com/images/I/91tYJTabe6L.png",
                        "video_image_width": "1920",
                        "video_image_height": "1080",
                        "video_image_extension": "png",
                        "video_url": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/v2/54907185-6217-5f34-acf3-fbdcc1366f93/ShortForm-Generic-480p-16-9-1409173089793-rpcbe5.mp4",
                        "video_previews": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/222710e4-1aab-4761-89f1-2680a5a2810a/videopreview.jobtemplate.mp4.342X192P_20HZ_350KBPS_VER_1_0.mp4,342X192P_20HZ_350KBPS_VER_1_0,video/mp4",
                        "video_mime_type": "video/mp4",
                        "duration": "0:46",
                        "closed_captions": "en,https://m.media-amazon.com/images/S/vse-vms-closed-captions-artifact-us-east-1-prod/closedCaptions/2de1a3dc-ab0d-42b1-ac3e-733d3ed2b478.vtt",
                        "type": "videos_for_this_product"
                    },
                    {
                        "id": "amzn1.vse.video.e8be75113656497fa6ddf8c2b6c178f2",
                        "product_asin": "B073JYC4XM",
                        "parent_asin": "B073JYC4XM",
                        "title": "Unboxing SanDisk Ultra 128GB ",
                        "profile_image_url": "https://www.amazon.com/avatar/default/amzn1.account.AHUVLVJCCVRN4BLRMDYZJN3CKGLA?max_width=110&square=True",
                        "profile_link": "/gp/profile/amzn1.account.AHUVLVJCCVRN4BLRMDYZJN3CKGLA",
                        "public_name": "LOON3YDG",
                        "creator_type": "Customer",
                        "vendor_code": "UGCPR",
                        "vendor_name": "LOON3YDG",
                        "video_image_id": "61sUrmhJ4+L",
                        "video_image_url": "https://m.media-amazon.com/images/I/61sUrmhJ4+L._CR0,0,1080,609_SR684,386_.jpg",
                        "video_image_url_unchanged": "https://m.media-amazon.com/images/I/61sUrmhJ4+L.jpg",
                        "video_image_width": "1080",
                        "video_image_height": "1920",
                        "video_image_extension": "jpg",
                        "video_url": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/bf1232b6-4f4f-4bfb-af80-2b093e402f2e/default.jobtemplate.hls.m3u8",
                        "video_previews": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/33ef8ad4-b76f-4553-b49f-efac9a5fc367/videopreview.jobtemplate.mp4.default.mp4,342X192P_20HZ_350KBPS_VER_1_0,video/mp4,https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/33ef8ad4-b76f-4553-b49f-efac9a5fc367/videopreview.jobtemplate.mp4.default.mp4,default,video/mp4",
                        "video_mime_type": "application/x-mpegURL",
                        "duration": "0:11",
                        "closed_captions": "en,https://m.media-amazon.com/images/S/vse-vms-closed-captions-artifact-us-east-1-prod/closedCaptions/d01323e1-6e1a-4943-8116-c987dbea2ee3.vtt",
                        "type": "videos_for_this_product"
                    },
                    {
                        "id": "amzn1.vse.video.0e0226f4f4cc40a1858bd9c6196f364f",
                        "product_asin": "B073JYC4XM",
                        "parent_asin": "B073JYC4XM",
                        "title": "I hope I don’t break it!",
                        "profile_image_url": "https://www.amazon.com/avatar/default/amzn1.account.AGEFKYA3ODAQVKMTESXS6QWYVZRA?max_width=110&square=True",
                        "profile_link": "/gp/profile/amzn1.account.AGEFKYA3ODAQVKMTESXS6QWYVZRA",
                        "public_name": "John Flynn",
                        "creator_type": "Customer",
                        "vendor_code": "UGCPR",
                        "vendor_name": "John Flynn",
                        "video_image_id": "B1p02KONkbS",
                        "video_image_url": "https://m.media-amazon.com/images/I/B1p02KONkbS._CR3,0,1914,1080_SR684,386_.png",
                        "video_image_url_unchanged": "https://images-na.ssl-images-amazon.com/images/I/B1p02KONkbS.png",
                        "video_image_width": "1920",
                        "video_image_height": "1080",
                        "video_image_extension": "png",
                        "video_url": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/v2/f662f612-c8c9-5e2a-8948-d5731af132e0/ShortForm-Generic-480p-16-9-1409173089793-rpcbe5.mp4",
                        "video_previews": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/d6acd4a1-f2a2-4b38-adb1-f4a4bbff33cc/videopreview.jobtemplate.mp4.342X192P_20HZ_350KBPS_VER_1_0.mp4,342X192P_20HZ_350KBPS_VER_1_0,video/mp4",
                        "video_mime_type": "video/mp4",
                        "duration": "0:16",
                        "closed_captions": "en,https://m.media-amazon.com/images/S/vse-vms-closed-captions-artifact-us-east-1-prod/closedCaptions/625326c1-9a12-4d58-b6c1-00fd87c43f2f.vtt",
                        "type": "videos_for_this_product"
                    },
                    {
                        "id": "amzn1.vse.video.6281a8545e3547e2b5dfd73cd93dbb0e",
                        "product_asin": "B073JYC4XM",
                        "parent_asin": "B073JYC4XM",
                        "title": "MicroSD and SD Memory card buying guide",
                        "profile_image_url": "https://images-na.ssl-images-amazon.com/images/S/influencer-profile-image-prod/logo/markdraper_1667551226117_original._FMjpg_.jpeg",
                        "profile_link": "/shop/markdraper",
                        "public_name": "Mark J Draper",
                        "creator_type": "Influencer",
                        "vendor_code": "markdraper:shop",
                        "vendor_name": "Mark J Draper",
                        "vendor_tracking_id": "amzvid-20 ",
                        "video_image_id": "81BFpuhrvjL",
                        "video_image_url": "https://m.media-amazon.com/images/I/81BFpuhrvjL._CR2,0,1196,675_SR684,386_.jpg",
                        "video_image_url_unchanged": "https://m.media-amazon.com/images/I/81BFpuhrvjL.jpg",
                        "video_image_width": "1200",
                        "video_image_height": "675",
                        "video_image_extension": "jpg",
                        "video_url": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/6c2e0f0d-8b64-4853-9c0a-c66d582a7fe1/default.jobtemplate.hls.m3u8",
                        "video_previews": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/086c90c7-a717-49c5-8f2b-788ea28572fb/videopreview.jobtemplate.mp4.342X192P_20HZ_350KBPS_VER_1_0.mp4,342X192P_20HZ_350KBPS_VER_1_0,video/mp4",
                        "video_mime_type": "application/x-mpegURL",
                        "duration": "2:17",
                        "closed_captions": "en,https://m.media-amazon.com/images/S/vse-vms-closed-captions-artifact-us-east-1-prod/closedCaptions/66cc81ba-613b-48be-a40b-cab3d65ff9e2.vtt",
                        "type": "videos_for_related_products"
                    },
                    {
                        "id": "amzn1.vse.video.0f9f71082c77417c9fb5468f1d3214db",
                        "product_asin": "B073JYC4XM",
                        "parent_asin": "B073JYC4XM",
                        "related_products": "B073JWXGNT, B08CLNX58K",
                        "title": "SanDisk Ultra micro SDHC UHS-I Memory Card with Adapter",
                        "profile_image_url": "https://images-na.ssl-images-amazon.com/images/S/influencer-profile-image-prod/midwestgardener_fa9671c9-59c4-424f-8747-f3105737475b.jpeg",
                        "profile_link": "/shop/midwestgardener",
                        "public_name": "Midwest Gardener",
                        "creator_type": "Influencer",
                        "vendor_code": "midwestgardener:shop",
                        "vendor_name": "Midwest Gardener",
                        "vendor_tracking_id": "onamzreptgems-20",
                        "video_image_id": "61N9XCe1IiL",
                        "video_image_url": "https://m.media-amazon.com/images/I/61N9XCe1IiL._CR1,0,638,360_SR342,193_.jpg",
                        "video_image_url_unchanged": "https://m.media-amazon.com/images/I/61N9XCe1IiL.jpg",
                        "video_image_width": "640",
                        "video_image_height": "360",
                        "video_image_extension": "jpg",
                        "video_url": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/d44dc4e0-558d-4a6e-81fa-9b365b6bf128/default.jobtemplate.hls.m3u8",
                        "video_previews": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/a8f012c1-6621-495a-8d3a-7202f4e2d77c/videopreview.jobtemplate.mp4.342X192P_20HZ_350KBPS_VER_1_0.mp4,342X192P_20HZ_350KBPS_VER_1_0,video/mp4",
                        "video_mime_type": "application/x-mpegURL",
                        "duration": "0:45",
                        "closed_captions": "en,https://m.media-amazon.com/images/S/vse-vms-closed-captions-artifact-us-east-1-prod/closedCaptions/34039046-c3fe-4024-8db6-d5a29dd9cb70.vtt",
                        "type": "videos_for_related_products"
                    },
                    {
                        "id": "amzn1.vse.video.0ea7d6eb1754445ca19f0fe77fd78b7a",
                        "product_asin": "B073JYC4XM",
                        "parent_asin": "B073JYC4XM",
                        "related_products": "B0758NHWS8, B08CLNX58K",
                        "title": "Which Memory card for DSLR cameras",
                        "profile_image_url": "https://images-na.ssl-images-amazon.com/images/S/influencer-profile-image-prod/logo/zulfphotography_1628065176720_original._CR0,0,1000,1000_._FMjpg_.png",
                        "profile_link": "/shop/zulfphotography",
                        "public_name": "Zulf - TrustedCreators",
                        "creator_type": "Influencer",
                        "vendor_code": "zulfphotography:shop",
                        "vendor_name": "Zulf - TrustedCreators",
                        "vendor_tracking_id": "zulfphotogr07-20",
                        "video_image_id": "71QMBYuT9RL",
                        "video_image_url": "https://m.media-amazon.com/images/I/71QMBYuT9RL._CR53,0,1839,1038_SR684,386_.jpg",
                        "video_image_url_unchanged": "https://m.media-amazon.com/images/I/71QMBYuT9RL.jpg",
                        "video_image_width": "1946",
                        "video_image_height": "1038",
                        "video_image_extension": "jpg",
                        "video_url": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/64497fd0-44be-4447-935d-0b3b6ab30074/default.jobtemplate.hls.m3u8",
                        "video_previews": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/3b579ed4-86bc-47be-8cdd-2e9e45d9ba48/videopreview.jobtemplate.mp4.342X192P_20HZ_350KBPS_VER_1_0.mp4,342X192P_20HZ_350KBPS_VER_1_0,video/mp4",
                        "video_mime_type": "application/x-mpegURL",
                        "duration": "0:33",
                        "closed_captions": "en,https://m.media-amazon.com/images/S/vse-vms-closed-captions-artifact-us-east-1-prod/closedCaptions/3e3cfc87-f921-4d83-8b5d-bd54f078759e.vtt",
                        "type": "videos_for_related_products"
                    },
                    {
                        "id": "amzn1.vse.video.0d90aeb405d04be7a35474e530480109",
                        "product_asin": "B073JYC4XM",
                        "parent_asin": "B073JYC4XM",
                        "related_products": "B08GYKNCCP, B074RNRM2B, B00M55C0NS, B015IYWJWO, B07B98GXQT",
                        "title": "Sandisk Ultra vs Samsung Pro Endurance Full Benchmark",
                        "profile_image_url": "https://images-na.ssl-images-amazon.com/images/S/influencer-profile-image-prod/logo/knowledgesharingtech_1648734401746_original._CR0,0,949,949_._FMjpg_.png",
                        "profile_link": "/shop/knowledgesharingtech",
                        "public_name": "Knowledge Sharing Tech",
                        "creator_type": "Influencer",
                        "vendor_code": "knowledgesharingtech:shop",
                        "vendor_name": "Knowledge Sharing Tech",
                        "vendor_tracking_id": "onamzknowle03-20",
                        "video_image_id": "91dTvFjcjsL",
                        "video_image_url": "https://m.media-amazon.com/images/I/91dTvFjcjsL._CR3,0,1914,1080_SR684,386_.png",
                        "video_image_url_unchanged": "https://m.media-amazon.com/images/I/91dTvFjcjsL.png",
                        "video_image_width": "1920",
                        "video_image_height": "1080",
                        "video_image_extension": "png",
                        "video_url": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/ae1a6e92-9ac5-4fa4-97c0-1b68275e17b7/default.jobtemplate.hls.m3u8",
                        "video_previews": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/ed32ae2d-6a07-4e1f-93f3-8bb7d9d201ae/videopreview.jobtemplate.mp4.342X192P_20HZ_350KBPS_VER_1_0.mp4,342X192P_20HZ_350KBPS_VER_1_0,video/mp4",
                        "video_mime_type": "application/x-mpegURL",
                        "duration": "2:19",
                        "closed_captions": "en,https://m.media-amazon.com/images/S/vse-vms-closed-captions-artifact-us-east-1-prod/closedCaptions/392a0010-f75c-49cd-bdf4-12a3ee696096.vtt",
                        "type": "videos_for_related_products"
                    },
                    {
                        "id": "amzn1.vse.video.059a04228b384857a8edc3e60d3171c1",
                        "product_asin": "B073JYC4XM",
                        "parent_asin": "B073JYC4XM",
                        "related_products": "B07FCMKK5X, B09V1FT19S",
                        "title": "SanDisk SD Card Review. Watch Before You Buy It!!",
                        "profile_image_url": "https://images-na.ssl-images-amazon.com/images/S/influencer-profile-image-prod/logo/influencer-b67ed546_1641652826852_original._CR0,0,1536,1536_._FMjpg_.jpeg",
                        "profile_link": "/shop/influencer-b67ed546",
                        "public_name": "Aaron SXS FURY",
                        "creator_type": "Influencer",
                        "vendor_code": "influencer-b67ed546:shop",
                        "vendor_name": "Aaron SXS FURY",
                        "vendor_tracking_id": "onamzsxsfury-20",
                        "video_image_id": "51KjqKwWurL",
                        "video_image_url": "https://m.media-amazon.com/images/I/51KjqKwWurL._CR1,0,638,360_SR342,193_.jpg",
                        "video_image_url_unchanged": "https://m.media-amazon.com/images/I/51KjqKwWurL.jpg",
                        "video_image_width": "640",
                        "video_image_height": "360",
                        "video_image_extension": "jpg",
                        "video_url": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/f150f7a2-ab5e-4a11-819a-283754588667/default.jobtemplate.hls.m3u8",
                        "video_previews": "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/db0339b3-a0d7-4ebc-914a-7d0eb03ff56e/videopreview.jobtemplate.mp4.342X192P_20HZ_350KBPS_VER_1_0.mp4,342X192P_20HZ_350KBPS_VER_1_0,video/mp4",
                        "video_mime_type": "application/x-mpegURL",
                        "duration": "1:25",
                        "closed_captions": "en,https://m.media-amazon.com/images/S/vse-vms-closed-captions-artifact-us-east-1-prod/closedCaptions/73f6de6d-cdf5-4199-a2b0-2a988d994c44.vtt",
                        "type": "videos_for_related_products"
                    }
                ],
                "is_bundle": False,
                "feature_bullets": [
                    "Ideal for Android Smartphones and Tablets. Certified to work with Chromebooks. (This product has been certified to meet Google’s compatibility standards. Chromebook and the “Works with Chromebook” badge are trademarks of Google LLC.)",
                    "Capacities up to 512GB (1GB=1,000,000,000 bytes. Actual user storage less) to store even more hours of Full HD video (Approximations; results and Full HD (1920x1080) video support may vary based on host device, file attributes and other factors.)",
                    "Up to 100MB/s transfer read speed (Based on internal testing; Performance may be lower depending on host device, interface, usage conditions and other factors.) lets you move up to 1000 photos in a minute (Based on 4.1GB transfer of photos (Average file 3.5MB) with USB 3.0 reader. Results may vary based on host device, file attributes and other factors.)",
                    "Load apps faster with A1-rated performance (A1 performance is 1500 read IOPS, 500 write IOPS. Based on internal testing. Results may vary based on host device, app type and other factors.)",
                    "Class 10 for Full HD video recording and playback (Full HD (1920x1080) video support may vary based upon host device, file attributes, and other factors.)",
                    "SanDisk Memory Zone app for easy file management (Download and Installation Required)",
                    "Order with your Alexa enabled device. Just ask \"Alexa, order SanDisk microSD.\""
                ],
                "feature_bullets_count": 7,
                "feature_bullets_flat": "Order with your Alexa enabled device. Just ask \"Alexa, order SanDisk microSD.\". SanDisk Memory Zone app for easy file management (Download and Installation Required). Class 10 for Full HD video recording and playback (Full HD (1920x1080) video support may vary based upon host device, file attributes, and other factors.). Load apps faster with A1-rated performance (A1 performance is 1500 read IOPS, 500 write IOPS. Based on internal testing. Results may vary based on host device, app type and other factors.). Up to 100MB/s transfer read speed (Based on internal testing; Performance may be lower depending on host device, interface, usage conditions and other factors.) lets you move up to 1000 photos in a minute (Based on 4.1GB transfer of photos (Average file 3.5MB) with USB 3.0 reader. Results may vary based on host device, file attributes and other factors.). Capacities up to 512GB (1GB=1,000,000,000 bytes. Actual user storage less) to store even more hours of Full HD video (Approximations; results and Full HD (1920x1080) video support may vary based on host device, file attributes and other factors.). Ideal for Android Smartphones and Tablets. Certified to work with Chromebooks. (This product has been certified to meet Google’s compatibility standards. Chromebook and the “Works with Chromebook” badge are trademarks of Google LLC.).",
                "attributes": [
                    {
                        "name": "Brand",
                        "value": "SanDisk"
                    },
                    {
                        "name": "Series",
                        "value": "SanDisk Ultra 128GB microSDXC UHS-I card with Adapter - SDSQUAR-128G-GN6MA"
                    },
                    {
                        "name": "Flash Memory Type",
                        "value": "Micro SD"
                    },
                    {
                        "name": "Memory Storage Capacity",
                        "value": "128 GB"
                    },
                    {
                        "name": "Compatible Devices",
                        "value": "Tablet, Smartphone"
                    }
                ],
                "top_reviews": [
                    {
                        "id": "R3F00K7CS1RMKT",
                        "title": "As Advertised",
                        "body": "The SD card came packaged and was new. (I bought it new so I couldn't expect less). Nonetheless, I need to become more familiar with SD Card home camera installation (but that's on me). Nevertheless, it's great and looks like it will last!  Thanks!Read more",
                        "body_html": "<div data-a-expander-name=\"review_text_read_more\" data-a-expander-collapsed-height=\"300\" class=\"a-expander-collapsed-height a-row a-expander-container a-expander-partial-collapse-container\" style=\"max-height:300px\"><div data-hook=\"review-collapsed\" aria-expanded=\"False\" class=\"a-expander-content reviewText review-text-content a-expander-partial-collapse-content\">             <span>The SD card came packaged and was new. (I bought it new so I couldn't expect less).<br>Nonetheless, I need to become more familiar with SD Card home camera installation (but that's on me).<br>Nevertheless, it's great and looks like it will last!<br><br>Thanks!</span>   </div><div class=\"a-expander-header a-expander-partial-collapse-header\"><div class=\"a-expander-content-fade\"></div><a href=\"javascript:void(0)\" data-csa-c-func-deps=\"aui-da-a-expander-toggle\" data-csa-c-type=\"widget\" data-csa-interaction-events=\"click\" data-hook=\"expand-collapse-read-more-less\" aria-label=\"Toggle full review text\" aria-expanded=\"False\" role=\"button\" data-action=\"a-expander-toggle\" class=\"a-declarative\" data-a-expander-toggle=\"{&quot;allowLinkDefault&quot;:True, &quot;expand_prompt&quot;:&quot;Read more&quot;, &quot;collapse_prompt&quot;:&quot;Read less&quot;}\"><i class=\"a-icon a-icon-extender-expand\"></i><span class=\"a-expander-prompt\">Read more</span></a></div></div>",
                        "link": "https://www.amazon.com/gp/customer-reviews/R3F00K7CS1RMKT/ref=cm_cr_dp_d_rvw_ttl?ie=UTF8&ASIN=B073JYC4XM",
                        "rating": 5,
                        "date": {
                            "raw": "Reviewed in the United States on February 24, 2023",
                            "utc": "2023-02-24T00:00:00.000Z"
                        },
                        "profile": {
                            "name": "Aurore F.",
                            "link": "https://www.amazon.com/gp/profile/amzn1.account.AH6AGUAHC4TMMZVQA5NZ3RTUFZ5Q/ref=cm_cr_dp_d_gw_tr?ie=UTF8",
                            "id": "AH6AGUAHC4TMMZVQA5NZ3RTUFZ5Q"
                        },
                        "vine_program": False,
                        "verified_purchase": True,
                        "review_country": "us",
                        "is_global_review": False
                    },
                    {
                        "id": "ROPW8TWWT5D7Z",
                        "title": "Doesn't actually have 128gb available, but that's normal.",
                        "body": "It's super easy to install into my Moto G stylus and I'd say most phones if not all. There's a space for micro SD cards by my sim card on the tray and you just place it in and push the tray back into the phone.  As I said in my title, it doesn't actually have 128gb of storage. Mine only has 119gb available. I suppose you could get super mad about that, but I really needed a larger SD card than a 32gb. So, I'm not complaining.  Also, with regular shipping it got here faster than I expected, so I was pretty happy about that.Read more",
                        "body_html": "<div data-a-expander-name=\"review_text_read_more\" data-a-expander-collapsed-height=\"300\" class=\"a-expander-collapsed-height a-row a-expander-container a-expander-partial-collapse-container\" style=\"max-height:300px\"><div data-hook=\"review-collapsed\" aria-expanded=\"False\" class=\"a-expander-content reviewText review-text-content a-expander-partial-collapse-content\">             <span>It's super easy to install into my Moto G stylus and I'd say most phones if not all. There's a space for micro SD cards by my sim card on the tray and you just place it in and push the tray back into the phone.<br><br>As I said in my title, it doesn't actually have 128gb of storage. Mine only has 119gb available. I suppose you could get super mad about that, but I really needed a larger SD card than a 32gb. So, I'm not complaining.<br><br>Also, with regular shipping it got here faster than I expected, so I was pretty happy about that.</span>   </div><div class=\"a-expander-header a-expander-partial-collapse-header\"><div class=\"a-expander-content-fade\"></div><a href=\"javascript:void(0)\" data-csa-c-func-deps=\"aui-da-a-expander-toggle\" data-csa-c-type=\"widget\" data-csa-interaction-events=\"click\" data-hook=\"expand-collapse-read-more-less\" aria-label=\"Toggle full review text\" aria-expanded=\"False\" role=\"button\" data-action=\"a-expander-toggle\" class=\"a-declarative\" data-a-expander-toggle=\"{&quot;allowLinkDefault&quot;:True, &quot;expand_prompt&quot;:&quot;Read more&quot;, &quot;collapse_prompt&quot;:&quot;Read less&quot;}\"><i class=\"a-icon a-icon-extender-expand\"></i><span class=\"a-expander-prompt\">Read more</span></a></div></div>",
                        "link": "https://www.amazon.com/gp/customer-reviews/ROPW8TWWT5D7Z/ref=cm_cr_dp_d_rvw_ttl?ie=UTF8&ASIN=B073JYC4XM",
                        "rating": 5,
                        "date": {
                            "raw": "Reviewed in the United States on January 4, 2023",
                            "utc": "2023-01-04T00:00:00.000Z"
                        },
                        "profile": {
                            "name": "Juls Neidermyer",
                            "link": "https://www.amazon.com/gp/profile/amzn1.account.AHVLYUIS452UDIMOYVJJZCKF5TJA/ref=cm_cr_dp_d_gw_tr?ie=UTF8",
                            "id": "AHVLYUIS452UDIMOYVJJZCKF5TJA",
                            "image": "https://images-na.ssl-images-amazon.com/images/S/amazon-avatars-global/de63cd44-0c60-4f24-9c59-d86b7a3d228e._CR0,0,375,375_SX48_.jpg"
                        },
                        "vine_program": True,
                        "vine_program_free_product": False,
                        "verified_purchase": True,
                        "review_country": "us",
                        "is_global_review": False
                    },
                    {
                        "id": "RBIVNBU9ZYGDD",
                        "title": "GREAT DRIVE, GREAT PRICE, FAST SHIPPING!!!!",
                        "body": "GREAT DRIVE, GREAT PRICE, FAST SHIPPING!!!!Read more",
                        "body_html": "<div data-a-expander-name=\"review_text_read_more\" data-a-expander-collapsed-height=\"300\" class=\"a-expander-collapsed-height a-row a-expander-container a-expander-partial-collapse-container\" style=\"max-height:300px\"><div data-hook=\"review-collapsed\" aria-expanded=\"False\" class=\"a-expander-content reviewText review-text-content a-expander-partial-collapse-content\">             <span>GREAT DRIVE, GREAT PRICE, FAST SHIPPING!!!!</span>   </div><div class=\"a-expander-header a-expander-partial-collapse-header\"><div class=\"a-expander-content-fade\"></div><a href=\"javascript:void(0)\" data-csa-c-func-deps=\"aui-da-a-expander-toggle\" data-csa-c-type=\"widget\" data-csa-interaction-events=\"click\" data-hook=\"expand-collapse-read-more-less\" aria-label=\"Toggle full review text\" aria-expanded=\"False\" role=\"button\" data-action=\"a-expander-toggle\" class=\"a-declarative\" data-a-expander-toggle=\"{&quot;allowLinkDefault&quot;:True, &quot;expand_prompt&quot;:&quot;Read more&quot;, &quot;collapse_prompt&quot;:&quot;Read less&quot;}\"><i class=\"a-icon a-icon-extender-expand\"></i><span class=\"a-expander-prompt\">Read more</span></a></div></div>",
                        "link": "https://www.amazon.com/gp/customer-reviews/RBIVNBU9ZYGDD/ref=cm_cr_dp_d_rvw_ttl?ie=UTF8&ASIN=B073JYC4XM",
                        "rating": 5,
                        "date": {
                            "raw": "Reviewed in the United States on February 21, 2023",
                            "utc": "2023-02-21T00:00:00.000Z"
                        },
                        "profile": {
                            "name": "jorge rodriguez",
                            "link": "https://www.amazon.com/gp/profile/amzn1.account.AHNOC63ANWYNJ2JNDZV7BFFCUIPQ/ref=cm_cr_dp_d_gw_tr?ie=UTF8",
                            "id": "AHNOC63ANWYNJ2JNDZV7BFFCUIPQ"
                        },
                        "vine_program": False,
                        "verified_purchase": True,
                        "review_country": "us",
                        "is_global_review": False
                    },
                    {
                        "id": "R1DIF8KWA029S7",
                        "title": "Reliable storage",
                        "body": "I am using two of these, in two security cameras. 4 months. They fill up with images, and the cameras reload over the oldest events. Cameras are outdoor.Read more",
                        "body_html": "<div data-a-expander-name=\"review_text_read_more\" data-a-expander-collapsed-height=\"300\" class=\"a-expander-collapsed-height a-row a-expander-container a-expander-partial-collapse-container\" style=\"max-height:300px\"><div data-hook=\"review-collapsed\" aria-expanded=\"False\" class=\"a-expander-content reviewText review-text-content a-expander-partial-collapse-content\">             <span>I am using two of these, in two security cameras. 4 months. They fill up with images, and the cameras reload over the oldest events. Cameras are outdoor.</span>   </div><div class=\"a-expander-header a-expander-partial-collapse-header\"><div class=\"a-expander-content-fade\"></div><a href=\"javascript:void(0)\" data-csa-c-func-deps=\"aui-da-a-expander-toggle\" data-csa-c-type=\"widget\" data-csa-interaction-events=\"click\" data-hook=\"expand-collapse-read-more-less\" aria-label=\"Toggle full review text\" aria-expanded=\"False\" role=\"button\" data-action=\"a-expander-toggle\" class=\"a-declarative\" data-a-expander-toggle=\"{&quot;allowLinkDefault&quot;:True, &quot;expand_prompt&quot;:&quot;Read more&quot;, &quot;collapse_prompt&quot;:&quot;Read less&quot;}\"><i class=\"a-icon a-icon-extender-expand\"></i><span class=\"a-expander-prompt\">Read more</span></a></div></div>",
                        "link": "https://www.amazon.com/gp/customer-reviews/R1DIF8KWA029S7/ref=cm_cr_dp_d_rvw_ttl?ie=UTF8&ASIN=B073JYC4XM",
                        "rating": 5,
                        "date": {
                            "raw": "Reviewed in the United States on February 2, 2023",
                            "utc": "2023-02-02T00:00:00.000Z"
                        },
                        "profile": {
                            "name": "Happy Square Trade Customer",
                            "link": "https://www.amazon.com/gp/profile/amzn1.account.AGEGRLKHDQYHUHK5CXEWREJVZ32Q/ref=cm_cr_dp_d_gw_tr?ie=UTF8",
                            "id": "AGEGRLKHDQYHUHK5CXEWREJVZ32Q"
                        },
                        "vine_program": False,
                        "verified_purchase": True,
                        "review_country": "us",
                        "is_global_review": False
                    },
                    {
                        "id": "R2VW4MDNNUIFNV",
                        "title": "Good product",
                        "body": "Works as designed..Read more",
                        "body_html": "<div data-a-expander-name=\"review_text_read_more\" data-a-expander-collapsed-height=\"300\" class=\"a-expander-collapsed-height a-row a-expander-container a-expander-partial-collapse-container\" style=\"max-height:300px\"><div data-hook=\"review-collapsed\" aria-expanded=\"False\" class=\"a-expander-content reviewText review-text-content a-expander-partial-collapse-content\">             <span>Works as designed..</span>   </div><div class=\"a-expander-header a-expander-partial-collapse-header\"><div class=\"a-expander-content-fade\"></div><a href=\"javascript:void(0)\" data-csa-c-func-deps=\"aui-da-a-expander-toggle\" data-csa-c-type=\"widget\" data-csa-interaction-events=\"click\" data-hook=\"expand-collapse-read-more-less\" aria-label=\"Toggle full review text\" aria-expanded=\"False\" role=\"button\" data-action=\"a-expander-toggle\" class=\"a-declarative\" data-a-expander-toggle=\"{&quot;allowLinkDefault&quot;:True, &quot;expand_prompt&quot;:&quot;Read more&quot;, &quot;collapse_prompt&quot;:&quot;Read less&quot;}\"><i class=\"a-icon a-icon-extender-expand\"></i><span class=\"a-expander-prompt\">Read more</span></a></div></div>",
                        "link": "https://www.amazon.com/gp/customer-reviews/R2VW4MDNNUIFNV/ref=cm_cr_dp_d_rvw_ttl?ie=UTF8&ASIN=B073JYC4XM",
                        "rating": 5,
                        "date": {
                            "raw": "Reviewed in the United States on February 19, 2023",
                            "utc": "2023-02-19T00:00:00.000Z"
                        },
                        "profile": {
                            "name": "mgr1604",
                            "link": "https://www.amazon.com/gp/profile/amzn1.account.AGHAZPFOQQN4DHAX57DIHJUX662Q/ref=cm_cr_dp_d_gw_tr?ie=UTF8",
                            "id": "AGHAZPFOQQN4DHAX57DIHJUX662Q",
                            "image": "https://images-na.ssl-images-amazon.com/images/S/amazon-avatars-global/6aaede32-7361-4662-a76b-db69de95633b._CR128,0,243,243_SX48_.jpg"
                        },
                        "vine_program": False,
                        "verified_purchase": True,
                        "review_country": "us",
                        "is_global_review": False
                    },
                    {
                        "id": "RV71SN1E57ZPJ",
                        "title": "hold a lot of information",
                        "body": "Easy to download.Read more",
                        "body_html": "<div data-a-expander-name=\"review_text_read_more\" data-a-expander-collapsed-height=\"300\" class=\"a-expander-collapsed-height a-row a-expander-container a-expander-partial-collapse-container\" style=\"max-height:300px\"><div data-hook=\"review-collapsed\" aria-expanded=\"False\" class=\"a-expander-content reviewText review-text-content a-expander-partial-collapse-content\">             <span>Easy to download.</span>   </div><div class=\"a-expander-header a-expander-partial-collapse-header\"><div class=\"a-expander-content-fade\"></div><a href=\"javascript:void(0)\" data-csa-c-func-deps=\"aui-da-a-expander-toggle\" data-csa-c-type=\"widget\" data-csa-interaction-events=\"click\" data-hook=\"expand-collapse-read-more-less\" aria-label=\"Toggle full review text\" aria-expanded=\"False\" role=\"button\" data-action=\"a-expander-toggle\" class=\"a-declarative\" data-a-expander-toggle=\"{&quot;allowLinkDefault&quot;:True, &quot;expand_prompt&quot;:&quot;Read more&quot;, &quot;collapse_prompt&quot;:&quot;Read less&quot;}\"><i class=\"a-icon a-icon-extender-expand\"></i><span class=\"a-expander-prompt\">Read more</span></a></div></div>",
                        "link": "https://www.amazon.com/gp/customer-reviews/RV71SN1E57ZPJ/ref=cm_cr_dp_d_rvw_ttl?ie=UTF8&ASIN=B073JYC4XM",
                        "rating": 5,
                        "date": {
                            "raw": "Reviewed in the United States on February 16, 2023",
                            "utc": "2023-02-16T00:00:00.000Z"
                        },
                        "profile": {
                            "name": "Larry Helms",
                            "link": "https://www.amazon.com/gp/profile/amzn1.account.AEFKRSGJ2KGRUCYXOA2PL4NXH3IA/ref=cm_cr_dp_d_gw_tr?ie=UTF8",
                            "id": "AEFKRSGJ2KGRUCYXOA2PL4NXH3IA"
                        },
                        "vine_program": False,
                        "verified_purchase": True,
                        "review_country": "us",
                        "is_global_review": False
                    },
                    {
                        "id": "R268IXSWKDVYZF",
                        "title": "Use in PI system memory",
                        "body": "works great with PI 4 computers.Read more",
                        "body_html": "<div data-a-expander-name=\"review_text_read_more\" data-a-expander-collapsed-height=\"300\" class=\"a-expander-collapsed-height a-row a-expander-container a-expander-partial-collapse-container\" style=\"max-height:300px\"><div data-hook=\"review-collapsed\" aria-expanded=\"False\" class=\"a-expander-content reviewText review-text-content a-expander-partial-collapse-content\">             <span>works great with PI 4 computers.</span>   </div><div class=\"a-expander-header a-expander-partial-collapse-header\"><div class=\"a-expander-content-fade\"></div><a href=\"javascript:void(0)\" data-csa-c-func-deps=\"aui-da-a-expander-toggle\" data-csa-c-type=\"widget\" data-csa-interaction-events=\"click\" data-hook=\"expand-collapse-read-more-less\" aria-label=\"Toggle full review text\" aria-expanded=\"False\" role=\"button\" data-action=\"a-expander-toggle\" class=\"a-declarative\" data-a-expander-toggle=\"{&quot;allowLinkDefault&quot;:True, &quot;expand_prompt&quot;:&quot;Read more&quot;, &quot;collapse_prompt&quot;:&quot;Read less&quot;}\"><i class=\"a-icon a-icon-extender-expand\"></i><span class=\"a-expander-prompt\">Read more</span></a></div></div>",
                        "link": "https://www.amazon.com/gp/customer-reviews/R268IXSWKDVYZF/ref=cm_cr_dp_d_rvw_ttl?ie=UTF8&ASIN=B073JYC4XM",
                        "rating": 5,
                        "date": {
                            "raw": "Reviewed in the United States on February 15, 2023",
                            "utc": "2023-02-15T00:00:00.000Z"
                        },
                        "profile": {
                            "name": "Bruce Ballew",
                            "link": "https://www.amazon.com/gp/profile/amzn1.account.AGYNBUEK25JSI2I2Z2CD2O33AVXA/ref=cm_cr_dp_d_gw_tr?ie=UTF8",
                            "id": "AGYNBUEK25JSI2I2Z2CD2O33AVXA"
                        },
                        "vine_program": False,
                        "verified_purchase": True,
                        "review_country": "us",
                        "is_global_review": False
                    },
                    {
                        "id": "RTGOOW9LIVLIA",
                        "title": "Great product !!",
                        "body": "Thank youRead more",
                        "body_html": "<div data-a-expander-name=\"review_text_read_more\" data-a-expander-collapsed-height=\"300\" class=\"a-expander-collapsed-height a-row a-expander-container a-expander-partial-collapse-container\" style=\"max-height:300px\"><div data-hook=\"review-collapsed\" aria-expanded=\"False\" class=\"a-expander-content reviewText review-text-content a-expander-partial-collapse-content\">             <span>Thank you</span>   </div><div class=\"a-expander-header a-expander-partial-collapse-header\"><div class=\"a-expander-content-fade\"></div><a href=\"javascript:void(0)\" data-csa-c-func-deps=\"aui-da-a-expander-toggle\" data-csa-c-type=\"widget\" data-csa-interaction-events=\"click\" data-hook=\"expand-collapse-read-more-less\" aria-label=\"Toggle full review text\" aria-expanded=\"False\" role=\"button\" data-action=\"a-expander-toggle\" class=\"a-declarative\" data-a-expander-toggle=\"{&quot;allowLinkDefault&quot;:True, &quot;expand_prompt&quot;:&quot;Read more&quot;, &quot;collapse_prompt&quot;:&quot;Read less&quot;}\"><i class=\"a-icon a-icon-extender-expand\"></i><span class=\"a-expander-prompt\">Read more</span></a></div></div>",
                        "link": "https://www.amazon.com/gp/customer-reviews/RTGOOW9LIVLIA/ref=cm_cr_dp_d_rvw_ttl?ie=UTF8&ASIN=B073JYC4XM",
                        "rating": 5,
                        "date": {
                            "raw": "Reviewed in the United States on February 15, 2023",
                            "utc": "2023-02-15T00:00:00.000Z"
                        },
                        "profile": {
                            "name": "Albert Ladon Green",
                            "link": "https://www.amazon.com/gp/profile/amzn1.account.AE2YZAGXNBSARGBUQV2IMYBZBTBQ/ref=cm_cr_dp_d_gw_tr?ie=UTF8",
                            "id": "AE2YZAGXNBSARGBUQV2IMYBZBTBQ"
                        },
                        "vine_program": False,
                        "verified_purchase": True,
                        "review_country": "us",
                        "is_global_review": False
                    },
                    {
                        "id": "R3KD6D4JFPT331",
                        "title": "I was sold a fake. I chose amazon as the retailer and I was still sold a fake.",
                        "body": "You can see from the screenshot I linked. The sd card starts corrupting data at 32gbs. This card is clearly a rebranded 32gb card with a False reporting controller. Be careful, test your cards.Read more",
                        "body_html": "<div data-a-expander-name=\"review_text_read_more\" data-a-expander-collapsed-height=\"300\" class=\"a-expander-collapsed-height a-row a-expander-container a-expander-partial-collapse-container\" style=\"max-height:300px\"><div data-hook=\"review-collapsed\" aria-expanded=\"False\" class=\"a-expander-content reviewText review-text-content a-expander-partial-collapse-content\">             <span>You can see from the screenshot I linked. The sd card starts corrupting data at 32gbs. This card is clearly a rebranded 32gb card with a False reporting controller. Be careful, test your cards.</span>   </div><div class=\"a-expander-header a-expander-partial-collapse-header\"><div class=\"a-expander-content-fade\"></div><a href=\"javascript:void(0)\" data-csa-c-func-deps=\"aui-da-a-expander-toggle\" data-csa-c-type=\"widget\" data-csa-interaction-events=\"click\" data-hook=\"expand-collapse-read-more-less\" aria-label=\"Toggle full review text\" aria-expanded=\"False\" role=\"button\" data-action=\"a-expander-toggle\" class=\"a-declarative\" data-a-expander-toggle=\"{&quot;allowLinkDefault&quot;:True, &quot;expand_prompt&quot;:&quot;Read more&quot;, &quot;collapse_prompt&quot;:&quot;Read less&quot;}\"><i class=\"a-icon a-icon-extender-expand\"></i><span class=\"a-expander-prompt\">Read more</span></a></div></div>",
                        "rating": 1,
                        "date": {
                            "raw": "Reviewed in Canada on November 13, 2018",
                            "utc": "2018-11-13T00:00:00.000Z"
                        },
                        "profile": {
                            "name": "brandon marino"
                        },
                        "vine_program": False,
                        "verified_purchase": True,
                        "helpful_votes": 1018,
                        "review_country": "ca",
                        "is_global_review": True
                    },
                    {
                        "id": "R6DMMX3SY57AK",
                        "title": "Fake microSD apparemment",
                        "body": "Class A1 pour une lecture rapide et ouverture des apps plus réactive sur smartphone. Le problème est que j'ai reçue une copie (fake) au lieu de l'originale. Sur l'original, l'opercule de sécurité est blanc, pas transparent et l'adaptateur SD n'a pas de relief (comme montré sur la page de l'article). En copie, les deux photos prises du produit reçu ainsi que la capture de l'adaptateur SD sur la page produit. Le SC Amazon m'envoie une nouvelle Micro SD et devrait investiguer le problème (merci à eux).Read more",
                        "body_html": "<div data-a-expander-name=\"review_text_read_more\" data-a-expander-collapsed-height=\"300\" class=\"a-expander-collapsed-height a-row a-expander-container a-expander-partial-collapse-container\" style=\"max-height:300px\"><div data-hook=\"review-collapsed\" aria-expanded=\"False\" class=\"a-expander-content reviewText review-text-content a-expander-partial-collapse-content\">           <span class=\"cr-original-review-content\">Class A1 pour une lecture rapide et ouverture des apps plus réactive sur smartphone. Le problème est que j'ai reçue une copie (fake) au lieu de l'originale. Sur l'original, l'opercule de sécurité est blanc, pas transparent et l'adaptateur SD n'a pas de relief (comme montré sur la page de l'article). En copie, les deux photos prises du produit reçu ainsi que la capture de l'adaptateur SD sur la page produit. Le SC Amazon m'envoie une nouvelle Micro SD et devrait investiguer le problème (merci à eux).</span><span class=\"cr-translated-review-content aok-hidden\"></span>     </div><div class=\"a-expander-header a-expander-partial-collapse-header\"><div class=\"a-expander-content-fade\"></div><a href=\"javascript:void(0)\" data-csa-c-func-deps=\"aui-da-a-expander-toggle\" data-csa-c-type=\"widget\" data-csa-interaction-events=\"click\" data-hook=\"expand-collapse-read-more-less\" aria-label=\"Toggle full review text\" aria-expanded=\"False\" role=\"button\" data-action=\"a-expander-toggle\" class=\"a-declarative\" data-a-expander-toggle=\"{&quot;allowLinkDefault&quot;:True, &quot;expand_prompt&quot;:&quot;Read more&quot;, &quot;collapse_prompt&quot;:&quot;Read less&quot;}\"><i class=\"a-icon a-icon-extender-expand\"></i><span class=\"a-expander-prompt\">Read more</span></a></div></div>",
                        "rating": 1,
                        "date": {
                            "raw": "Reviewed in France on October 12, 2018",
                            "utc": "2018-10-12T00:00:00.000Z"
                        },
                        "profile": {
                            "name": "MH"
                        },
                        "vine_program": False,
                        "verified_purchase": True,
                        "helpful_votes": 657,
                        "review_country": "fr",
                        "is_global_review": True
                    },
                    {
                        "id": "R1PVB2T00PS154",
                        "title": "UPDATED-",
                        "body": "*Orig review* Bought to use in my Android phone to increase storage space; have successfully transferred all my data across and couldn't be happier. The actual transfer process was fast for memory card standards imo. The SD card reader is a bonus, though slightly useless for me as I have a few already. SanDisk is always my go to for SD cards and I don't think they'll have disappointed this time either. If you're undecided on what size to get- definitely go for the larger one as I did.  *UPDATE* Previously 5 stars but have decreased as this SD card failed on me after about 8 months. Annoying as I can't retrieve the files I had stored on there , though luckily I had backups elsewhere too. Will see if there is a warranty as it wasn't the cheapest.Read more",
                        "body_html": "<div data-a-expander-name=\"review_text_read_more\" data-a-expander-collapsed-height=\"300\" class=\"a-expander-collapsed-height a-row a-expander-container a-expander-partial-collapse-container\" style=\"max-height:300px\"><div data-hook=\"review-collapsed\" aria-expanded=\"False\" class=\"a-expander-content reviewText review-text-content a-expander-partial-collapse-content\">             <span>*Orig review*<br>Bought to use in my Android phone to increase storage space; have successfully transferred all my data across and couldn't be happier. The actual transfer process was fast for memory card standards imo. The SD card reader is a bonus, though slightly useless for me as I have a few already. SanDisk is always my go to for SD cards and I don't think they'll have disappointed this time either. If you're undecided on what size to get- definitely go for the larger one as I did.<br><br>*UPDATE* Previously 5 stars but have decreased as this SD card failed on me after about 8 months. Annoying as I can't retrieve the files I had stored on there , though luckily I had backups elsewhere too. Will see if there is a warranty as it wasn't the cheapest.</span>   </div><div class=\"a-expander-header a-expander-partial-collapse-header\"><div class=\"a-expander-content-fade\"></div><a href=\"javascript:void(0)\" data-csa-c-func-deps=\"aui-da-a-expander-toggle\" data-csa-c-type=\"widget\" data-csa-interaction-events=\"click\" data-hook=\"expand-collapse-read-more-less\" aria-label=\"Toggle full review text\" aria-expanded=\"False\" role=\"button\" data-action=\"a-expander-toggle\" class=\"a-declarative\" data-a-expander-toggle=\"{&quot;allowLinkDefault&quot;:True, &quot;expand_prompt&quot;:&quot;Read more&quot;, &quot;collapse_prompt&quot;:&quot;Read less&quot;}\"><i class=\"a-icon a-icon-extender-expand\"></i><span class=\"a-expander-prompt\">Read more</span></a></div></div>",
                        "rating": 2,
                        "date": {
                            "raw": "Reviewed in the United Kingdom on June 9, 2018",
                            "utc": "2018-06-09T00:00:00.000Z"
                        },
                        "profile": {
                            "name": "ZM~"
                        },
                        "vine_program": False,
                        "verified_purchase": True,
                        "helpful_votes": 395,
                        "review_country": "gb",
                        "is_global_review": True
                    },
                    {
                        "id": "R8S78HXYK4D6E",
                        "title": "Ideal para la Switch.",
                        "body": "Una tarjeta de gran capacidad y muy fiable.  Suele estar muy bien de precio. Compré la de 200 gigas a finales de 2017 para usarla en la Switch, y un año después he comprado la de 128.  La tarjeta viene en formato exFat, aunque para usar en la Switch conviene formatearla en Fat32, no porque sea mejor sistema (que no lo es), sino porque la implementación del exFat en la Switch es bastante malo, y es más habitual que se produzca corrupción de datos que en Fat32, sobre todo si usas homebrew.  La corrupción de datos no es nada grave, pero sí muy molesta, y puede obligarte a reinstalar un juego, o puede hacerte perder las partidas salvadas. Esto, repito, en caso de usar homebrew. Con un uso normal y apagando la consola antes de insertar o retirar la tarjeta, no hay problemas.  Por si estáis interesados en formatear la tarjeta en Fat32, Windows no permite hacerlo en tarjetas tan grandes, así que tendréis que usar la aplicación \"guiformat\".  Espero que os sirva de ayuda.Read more",
                        "body_html": "<div data-a-expander-name=\"review_text_read_more\" data-a-expander-collapsed-height=\"300\" class=\"a-expander-collapsed-height a-row a-expander-container a-expander-partial-collapse-container\" style=\"max-height:300px\"><div data-hook=\"review-collapsed\" aria-expanded=\"False\" class=\"a-expander-content reviewText review-text-content a-expander-partial-collapse-content\">           <span class=\"cr-original-review-content\">Una tarjeta de gran capacidad y muy fiable.<br><br>Suele estar muy bien de precio. Compré la de 200 gigas a finales de 2017 para usarla en la Switch, y un año después he comprado la de 128.<br><br>La tarjeta viene en formato exFat, aunque para usar en la Switch conviene formatearla en Fat32, no porque sea mejor sistema (que no lo es), sino porque la implementación del exFat en la Switch es bastante malo, y es más habitual que se produzca corrupción de datos que en Fat32, sobre todo si usas homebrew.<br><br>La corrupción de datos no es nada grave, pero sí muy molesta, y puede obligarte a reinstalar un juego, o puede hacerte perder las partidas salvadas. Esto, repito, en caso de usar homebrew. Con un uso normal y apagando la consola antes de insertar o retirar la tarjeta, no hay problemas.<br><br>Por si estáis interesados en formatear la tarjeta en Fat32, Windows no permite hacerlo en tarjetas tan grandes, así que tendréis que usar la aplicación \"guiformat\".<br><br>Espero que os sirva de ayuda.</span><span class=\"cr-translated-review-content aok-hidden\"></span>     </div><div class=\"a-expander-header a-expander-partial-collapse-header\"><div class=\"a-expander-content-fade\"></div><a href=\"javascript:void(0)\" data-csa-c-func-deps=\"aui-da-a-expander-toggle\" data-csa-c-type=\"widget\" data-csa-interaction-events=\"click\" data-hook=\"expand-collapse-read-more-less\" aria-label=\"Toggle full review text\" aria-expanded=\"False\" role=\"button\" data-action=\"a-expander-toggle\" class=\"a-declarative\" data-a-expander-toggle=\"{&quot;allowLinkDefault&quot;:True, &quot;expand_prompt&quot;:&quot;Read more&quot;, &quot;collapse_prompt&quot;:&quot;Read less&quot;}\"><i class=\"a-icon a-icon-extender-expand\"></i><span class=\"a-expander-prompt\">Read more</span></a></div></div>",
                        "rating": 5,
                        "date": {
                            "raw": "Reviewed in Spain on December 11, 2018",
                            "utc": "2018-12-11T00:00:00.000Z"
                        },
                        "profile": {
                            "name": "jedeitor"
                        },
                        "vine_program": False,
                        "verified_purchase": True,
                        "helpful_votes": 388,
                        "review_country": "es",
                        "is_global_review": True
                    },
                    {
                        "id": "R3LAQM574R3YFM",
                        "title": "perfect for my Nintendo switch (also doesn’t affect the games ...",
                        "body": "Read a lot of reviews saying they’re second hand and had stuff on them already, but I can confirm mine was in brand new packaging and had no scratches and no data on it, perfect for my Nintendo switch (also doesn’t affect the games play speed either, definitely recommend purchasing instead of the overpriced Nintendo one)Read more",
                        "body_html": "<div data-a-expander-name=\"review_text_read_more\" data-a-expander-collapsed-height=\"300\" class=\"a-expander-collapsed-height a-row a-expander-container a-expander-partial-collapse-container\" style=\"max-height:300px\"><div data-hook=\"review-collapsed\" aria-expanded=\"False\" class=\"a-expander-content reviewText review-text-content a-expander-partial-collapse-content\">             <span>Read a lot of reviews saying they’re second hand and had stuff on them already, but I can confirm mine was in brand new packaging and had no scratches and no data on it, perfect for my Nintendo switch (also doesn’t affect the games play speed either, definitely recommend purchasing instead of the overpriced Nintendo one)</span>   </div><div class=\"a-expander-header a-expander-partial-collapse-header\"><div class=\"a-expander-content-fade\"></div><a href=\"javascript:void(0)\" data-csa-c-func-deps=\"aui-da-a-expander-toggle\" data-csa-c-type=\"widget\" data-csa-interaction-events=\"click\" data-hook=\"expand-collapse-read-more-less\" aria-label=\"Toggle full review text\" aria-expanded=\"False\" role=\"button\" data-action=\"a-expander-toggle\" class=\"a-declarative\" data-a-expander-toggle=\"{&quot;allowLinkDefault&quot;:True, &quot;expand_prompt&quot;:&quot;Read more&quot;, &quot;collapse_prompt&quot;:&quot;Read less&quot;}\"><i class=\"a-icon a-icon-extender-expand\"></i><span class=\"a-expander-prompt\">Read more</span></a></div></div>",
                        "rating": 5,
                        "date": {
                            "raw": "Reviewed in the United Kingdom on March 12, 2018",
                            "utc": "2018-03-12T00:00:00.000Z"
                        },
                        "profile": {
                            "name": "Dionne Hampson",
                            "image": "https://images-eu.ssl-images-amazon.com/images/S/amazon-avatars-global/e88d71db-fc15-48eb-ba05-d9bf04d775f9._CR0,26.0,281,281_SX48_.jpg"
                        },
                        "vine_program": False,
                        "verified_purchase": True,
                        "helpful_votes": 257,
                        "review_country": "gb",
                        "is_global_review": True
                    }
                ],
                "buybox_winner": {
                    "maximum_order_quantity": {
                        "value": 100,
                        "hard_maximum": True
                    },
                    "offer_id": "iUHo1Dph5hRpVeV4B5ny8RPGXmt37/ZVkvsBi80PtyCWwZyGhG8cesh3sbQW9BndafcH6/ne9gYdnIL6YrntyDk7yrSYpaTOqM1+7rH9uDpHLyCuLQY6j05psbhzjIOpkMPnvpjhsyPgnspqtsQOL2gKSWMMnlazpnwg8RbSjFeEUcGyBBpmVl9miOOmkslT",
                    "mixed_offers_count": 15,
                    "mixed_offers_from": {
                        "symbol": "$",
                        "value": 25,
                        "currency": "USD",
                        "raw": "FREE Shipping on orders over $25.00 shipped by Amazon."
                    },
                    "is_prime": True,
                    "is_amazon_fresh": False,
                    "condition": {
                        "is_new": True
                    },
                    "availability": {
                        "type": "in_stock",
                        "raw": "In Stock",
                        "dispatch_days": 1
                    },
                    "fulfillment": {
                        "type": "2p",
                        "standard_delivery": {
                            "date": "Wednesday, March 8",
                            "name": "FREE"
                        },
                        "is_sold_by_amazon": False,
                        "is_fulfilled_by_amazon": True,
                        "is_fulfilled_by_third_party": False,
                        "is_sold_by_third_party": True,
                        "third_party_seller": {
                            "name": "Nityamaa",
                            "link": "https://www.amazon.com/gp/help/seller/at-a-glance.html/ref=dp_merchant_link?ie=UTF8&seller=A30R1DDXV5VUEV&asin=B073JYC4XM&ref_=dp_merchant_link&isAmazonFulfilled=1",
                            "id": "A30R1DDXV5VUEV"
                        }
                    },
                    "price": {
                        "symbol": "$",
                        "value": 14.7,
                        "currency": "USD",
                        "raw": "$14.70"
                    },
                    "rrp": {
                        "symbol": "$",
                        "value": 49.99,
                        "currency": "USD",
                        "raw": "$49.99"
                    },
                    "shipping": {
                        "raw": "FREE"
                    }
                },
                "more_buying_choices": [
                    {
                        "price": {
                            "symbol": "$",
                            "value": 14.7,
                            "currency": "USD",
                            "raw": "$14.70"
                        },
                        "seller_name": "Prime-Pros",
                        "seller_link": "https://www.amazon.com/gp/aag/main?ie=UTF8&seller=A2TWIRHLRS9O1T&isAmazonFulfilled=1&asin=B073JYC4XM&ref_=dp_mbc_seller",
                        "free_shipping": True,
                        "position": 1
                    },
                    {
                        "price": {
                            "symbol": "$",
                            "value": 15.47,
                            "currency": "USD",
                            "raw": "$15.47"
                        },
                        "seller_name": "First Choice Online",
                        "seller_link": "https://www.amazon.com/gp/aag/main?ie=UTF8&seller=A35BKAA6VXTYCT&isAmazonFulfilled=1&asin=B073JYC4XM&ref_=dp_mbc_seller",
                        "free_shipping": True,
                        "position": 2
                    },
                    {
                        "price": {
                            "symbol": "$",
                            "value": 15.5,
                            "currency": "USD",
                            "raw": "$15.50"
                        },
                        "seller_name": "Mobile deals",
                        "seller_link": "https://www.amazon.com/gp/aag/main?ie=UTF8&seller=A2HD8Q5HC778I7&isAmazonFulfilled=1&asin=B073JYC4XM&ref_=dp_mbc_seller",
                        "free_shipping": True,
                        "position": 3
                    }
                ],
                "specifications": [
                    {
                        "name": "RAM",
                        "value": "‎128 GB"
                    },
                    {
                        "name": "Memory Speed",
                        "value": "‎100 Megabytes Per Second"
                    },
                    {
                        "name": "Brand",
                        "value": "‎SanDisk"
                    },
                    {
                        "name": "Series",
                        "value": "‎SanDisk Ultra 128GB microSDXC UHS-I card with Adapter - SDSQUAR-128G-GN6MA"
                    },
                    {
                        "name": "Item model number",
                        "value": "‎SDSQUAR-128G-GN6MA"
                    },
                    {
                        "name": "Item Weight",
                        "value": "‎0.16 ounces"
                    },
                    {
                        "name": "Product Dimensions",
                        "value": "‎0.03 x 0.59 x 0.43 inches"
                    },
                    {
                        "name": "Item Dimensions  LxWxH",
                        "value": "‎0.03 x 0.59 x 0.43 inches"
                    },
                    {
                        "name": "Color",
                        "value": "‎Grey,Red, Grey"
                    },
                    {
                        "name": "Department",
                        "value": "‎Memory"
                    },
                    {
                        "name": "Manufacturer",
                        "value": "‎Western Digital Technologies Inc."
                    },
                    {
                        "name": "ASIN",
                        "value": "‎B073JYC4XM"
                    },
                    {
                        "name": "Is Discontinued By Manufacturer",
                        "value": "‎No"
                    },
                    {
                        "name": "Date First Available",
                        "value": "‎August 3, 2017"
                    },
                    {
                        "name": "Customer Reviews",
                        "value": "4.7 out of 5 stars       216,211 ratings          4.7 out of 5 stars"
                    },
                    {
                        "name": "Best Sellers Rank",
                        "value": "#34 in Micro SD Memory Cards"
                    },
                    {
                        "name": "Brand",
                        "value": "SanDisk"
                    },
                    {
                        "name": "Series",
                        "value": "SanDisk Ultra 128GB microSDXC UHS-I card with Adapter - SDSQUAR-128G-GN6MA"
                    },
                    {
                        "name": "Flash Memory Type",
                        "value": "Micro SD"
                    },
                    {
                        "name": "Memory Storage Capacity",
                        "value": "128 GB"
                    },
                    {
                        "name": "Compatible Devices",
                        "value": "Tablet, Smartphone"
                    }
                ],
                "specifications_flat": "Compatible Devices: Tablet, Smartphone. Memory Storage Capacity: 128 GB. Flash Memory Type: Micro SD. Series: SanDisk Ultra 128GB microSDXC UHS-I card with Adapter - SDSQUAR-128G-GN6MA. Brand: SanDisk. Best Sellers Rank: #34 in Micro SD Memory Cards. Customer Reviews: 4.7 out of 5 stars       216,211 ratings          4.7 out of 5 stars. Date First Available: ‎August 3, 2017. Is Discontinued By Manufacturer: ‎No. ASIN: ‎B073JYC4XM. Manufacturer: ‎Western Digital Technologies Inc. Department: ‎Memory. Color: ‎Grey,Red, Grey. Item Dimensions  LxWxH: ‎0.03 x 0.59 x 0.43 inches. Product Dimensions: ‎0.03 x 0.59 x 0.43 inches. Item Weight: ‎0.16 ounces. Item model number: ‎SDSQUAR-128G-GN6MA. Series: ‎SanDisk Ultra 128GB microSDXC UHS-I card with Adapter - SDSQUAR-128G-GN6MA. Brand: ‎SanDisk. Memory Speed: ‎100 Megabytes Per Second. RAM: ‎128 GB.",
                "bestsellers_rank": [
                    {
                        "category": "Micro SD Memory Cards",
                        "rank": 34,
                        "link": "https://www.amazon.com/gp/bestsellers/pc/3015433011/ref=pd_zg_hrsr_pc"
                    }
                ],
                "color": "‎Grey,Red, Grey",
                "manufacturer": "‎Western Digital Technologies Inc.",
                "weight": "‎0.16 ounces",
                "first_available": "‎August 3, 2017",
                "dimensions": "‎0.03 x 0.59 x 0.43 inches",
                "model_number": "‎SDSQUAR-128G-GN6MA",
                "bestsellers_rank_flat": "Category: Micro SD Memory Cards | Rank: 34",
                "whats_in_the_box": [
                    "SanDisk Ultra microSDXC UHS-I Card",
                    "SD adapter"
                ]
            },
            "brand_store": {
                "id": "CD971F4B-EE23-4EA1-96E3-567678AC9C0A",
                "link": "https://www.amazon.com/stores/SanDisk/page/CD971F4B-EE23-4EA1-96E3-567678AC9C0A"
            },
            "user_guide": "https://m.media-amazon.com/images/I/91NqBqLsumS.pdf",
            "newer_model": {
                "title": "SanDisk 128GB Ultra microSDXC UHS-I Memory Card with Adapter - Up to 140MB/s, C10, U1, Full HD, A1, MicroSD Card - SDSQUAB-128G-GN6MA",
                "asin": "B0B7NTY2S6",
                "link": "https://www.amazon.com/SanDisk-128GB-microSDXC-Memory-Adapter-dp-B0B7NTY2S6/dp/B0B7NTY2S6/ref=dp_ob_image_ce",
                "image": "https://m.media-amazon.com/images/I/51h4FuIul3L._SR75,75_.jpg",
                "rating": 4.5,
                "ratings_total": 104942,
                "price": {
                    "raw": "$13.99Only 2 left in stock - order soon."
                }
            },
            "frequently_bought_together": {
                "total_price": {
                    "symbol": "$",
                    "value": 76.68,
                    "currency": "USD",
                    "raw": "$76.68"
                },
                "products": [
                    {
                        "asin": "B073JYC4XM",
                        "title": "TRIDENITE 64GB Micro SD Card, MicroSDXC Memory for Nintendo-Switch, GoPro, Drone, Smartphone, Tablet, 4K Ultra HD, A1 UHS-I U3 V30 C10, Up to 95MB/s Read, with SD Adapter",
                        "link": "https://www.amazon.com/dp/B073JYC4XM",
                        "image": "https://images-na.ssl-images-amazon.com/images/G/01/x-locale/common/grey-pixel.gif",
                        "price": {
                            "symbol": "$",
                            "value": 14.7,
                            "currency": "USD",
                            "raw": "$14.70"
                        }
                    }
                ]
            },
            "compare_with_similar": [
                {
                    "asin": "B073JYC4XM",
                    "image": "https://m.media-amazon.com/images/I/617NtexaW2L._AC_SS450_.jpg",
                    "title": "SanDisk 128GB Ultra MicroSDXC UHS-I Memory Card with Adapter - 100MB/s, C10, U1, Full HD, A1, Micro SD Card - SDSQUAR-128G-GN6MA",
                    "rating": 4.5,
                    "ratings_total": 216211,
                    "price": {
                        "symbol": "$",
                        "value": 14.7,
                        "currency": "USD",
                        "raw": "$14.70"
                    },
                    "link": "https://www.amazon.com/dp/B073JYC4XM"
                },
                {
                    "asin": "B09RWWKM5D",
                    "image": "https://m.media-amazon.com/images/I/51ji2nUCtQL._AC_SS450_.jpg",
                    "title": "TRIDENITE 64GB Micro SD Card, MicroSDXC Memory for Nintendo-Switch, GoPro, Drone, Smartphone, Tablet, 4K Ultra HD, A1 UHS-I U3 V30 C10, Up to 95MB/s Read, with SD Adapter",
                    "rating": 4.5,
                    "ratings_total": 1267,
                    "price": {
                        "symbol": "$",
                        "value": 6.9,
                        "currency": "USD",
                        "raw": "$6.90"
                    },
                    "link": "https://www.amazon.com/dp/B09RWWKM5D"
                },
                {
                    "asin": "B07VS8WFF4",
                    "image": "https://m.media-amazon.com/images/I/51cUGYwMJmL._AC_SS450_.jpg",
                    "title": "AXE MEMORY 64GB microSDXC Memory Card + SD Adapter with A1 App Performance, V30 UHS-I U3 4K",
                    "rating": 4.5,
                    "ratings_total": 10995,
                    "price": {
                        "symbol": "$",
                        "value": 8.99,
                        "currency": "USD",
                        "raw": "$8.99"
                    },
                    "link": "https://www.amazon.com/dp/B07VS8WFF4"
                },
                {
                    "asin": "B07VQ2B72D",
                    "image": "https://m.media-amazon.com/images/I/511kSw750CL._AC_SS450_.jpg",
                    "title": "AXE MEMORY 64GB microSDXC Memory Card + SD Adapter with A2 App Performance, V30 UHS-I U3 4K",
                    "rating": 4.5,
                    "ratings_total": 10995,
                    "price": {
                        "symbol": "$",
                        "value": 12.99,
                        "currency": "USD",
                        "raw": "$12.99"
                    },
                    "link": "https://www.amazon.com/dp/B07VQ2B72D"
                },
                {
                    "asin": "B09QS7P8HH",
                    "image": "https://m.media-amazon.com/images/I/51FfP81xAbL._AC_SS450_.jpg",
                    "title": "Espeon Micro SD Card 64GB with SD Adapter for Smartphone and Tablet MicroSDXC Memory Expansion, Nintendo-Switch, Portable Game Consoles. 4K Video Playback, A1 UHS-I U3 V30 C10, Up to 95MB/s Read",
                    "rating": 4.5,
                    "ratings_total": 641,
                    "price": {
                        "symbol": "$",
                        "value": 8.99,
                        "currency": "USD",
                        "raw": "$8.99"
                    },
                    "link": "https://www.amazon.com/dp/B09QS7P8HH"
                },
                {
                    "asin": "B073JYVKNX",
                    "image": "https://m.media-amazon.com/images/I/7180ZAZmERL._AC_SS450_.jpg",
                    "title": "SanDisk 64GB Ultra MicroSDXC UHS-I Memory Card with Adapter - 100MB/s, C10, U1, Full HD, A1, Micro SD Card - SDSQUAR-064G-GN6MA",
                    "rating": 4.5,
                    "ratings_total": 400424,
                    "price": {
                        "symbol": "$",
                        "value": 10.2,
                        "currency": "USD",
                        "raw": "$10.20"
                    },
                    "link": "https://www.amazon.com/dp/B073JYVKNX"
                }
            ]
        }
