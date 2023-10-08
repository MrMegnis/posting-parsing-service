import unittest
import requests


class Tester(unittest.TestCase):
    def setUp(self) -> None:
        self.root = "http://127.0.0.1:3000"

    def test0(self):
        url = f"{self.root}/users"
        data = {
            "tg_id": 12345
        }
        # ----------
        response = requests.post(url, json=data)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        ans = response.json()
        self.assertEqual(ans["result"][0], "Success")
        ans = ans["result"][1]["created_user"]
        print(ans)
        self.assertEqual(ans["tg_id"], 12345)
        self.assertEqual(ans["orders_amount"], 0)
        self.assertEqual(ans["is_VIP"], False)
        url = f"{self.root}/users/by_tg/12345"
        response = requests.get(url)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        ans = response.json()
        ans = ans["user"]
        self.assertEqual(ans["tg_id"], 12345)
        self.assertEqual(ans["orders_amount"], 0)
        self.assertEqual(ans["is_VIP"], False)
        # -----------
        url = f"{self.root}/users/by_tg/12345"
        data = {
            "orders_amount": 123,
            "is_VIP": True
        }
        response = requests.put(url, json=data)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        ans = response.json()
        self.assertEqual(ans["result"][0], "Success")
        ans = ans["result"][1]["updated_user"]
        print(ans)
        self.assertEqual(ans["tg_id"], 12345)
        self.assertEqual(ans["orders_amount"], 123)
        self.assertEqual(ans["is_VIP"], True)
        url = f"{self.root}/users/by_tg/12345"
        response = requests.get(url)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        ans = response.json()
        ans = ans["user"]
        self.assertEqual(ans["tg_id"], 12345)
        self.assertEqual(ans["orders_amount"], 123)
        self.assertEqual(ans["is_VIP"], True)
        # -----------
        url = f"{self.root}/users/by_tg/12345"
        response = requests.delete(url)
        self.assertEqual(response.status_code, 200)
        print(response.json())
        ans = response.json()
        self.assertEqual(ans["result"], "Success")

    def test1(self):
        url = f"{self.root}/users"
        data = list()
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 400)
        data = dict()
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 400)
        data = {
            "tg_id": 12345
        }
        response = requests.post(url, json=data)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 413)
        url = f"{self.root}/users/by_tg/12345"
        response = requests.delete(url)
        self.assertEqual(response.status_code, 200)
        print(response.json())
        ans = response.json()
        self.assertEqual(ans["result"], "Success")

    def test2(self):
        url = f"{self.root}/users"
        data1 = {
            "tg_id": 12345
        }
        data2 = {
            "tg_id": 54321
        }
        # ----------create_user
        response = requests.post(url, json=data1)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        ans = response.json()
        self.assertEqual(ans["result"][0], "Success")
        ans = ans["result"][1]["created_user"]
        print(ans)
        self.assertEqual(ans["tg_id"], 12345)
        self.assertEqual(ans["orders_amount"], 0)
        self.assertEqual(ans["is_VIP"], False)
        # -----------get_user
        url = f"{self.root}/users/by_tg/12345"
        response = requests.get(url)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        ans = response.json()
        ans = ans["user"]
        self.assertEqual(ans["tg_id"], 12345)
        self.assertEqual(ans["orders_amount"], 0)
        self.assertEqual(ans["is_VIP"], False)
        # -----------create_order
        url = f"{self.root}/orders"
        data = {
            "user_tg_id": 12345,
            "name": "MyOrder",
            "vk_group_id": -22222,
            "interval": 60,
            "left_days": 100,
            "last_post_id": 123
        }
        response = requests.post(url, json=data)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        ans = response.json()
        self.assertEqual(ans["result"][0], "Success")
        ans = ans["result"][1]["created_order"]
        print(ans)
        self.assertEqual(ans["name"], "MyOrder")
        self.assertEqual(ans["vk_group_id"], -22222)
        self.assertEqual(ans["interval"], 60)
        self.assertEqual(ans["left_days"], 100)
        self.assertEqual(ans["last_post_id"], 123)
        id_ = ans["id"]
        # -----------get_order
        url = f"{self.root}/orders/{id_}"
        response = requests.get(url)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        ans = response.json()
        ans = ans["order"]
        self.assertEqual(ans["name"], "MyOrder")
        self.assertEqual(ans["vk_group_id"], -22222)
        self.assertEqual(ans["interval"], 60)
        self.assertEqual(ans["left_days"], 100)
        self.assertEqual(ans["last_post_id"], 123)
        # -----------get_order
        url = f"{self.root}/orders/by_name/MyOrder"
        response = requests.get(url)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        ans = response.json()
        ans = ans["order"]
        self.assertEqual(ans["name"], "MyOrder")
        self.assertEqual(ans["vk_group_id"], -22222)
        self.assertEqual(ans["interval"], 60)
        self.assertEqual(ans["left_days"], 100)
        self.assertEqual(ans["last_post_id"], 123)
        # -----------get_user
        url = f"{self.root}/users/by_tg/12345"
        response = requests.get(url)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        ans = response.json()
        ans = ans["user"]
        self.assertEqual(ans["tg_id"], 12345)
        self.assertEqual(ans["orders_amount"], 1)
        self.assertEqual(ans["is_VIP"], False)
        # -----------update_order
        url = f"{self.root}/orders/{id_}"
        data = {
            "name": "MyCoolOrder",
            "vk_group_id": -33333,
            "interval": 120,
            "left_days": 50,
            "last_post_id": 1000
        }
        response = requests.put(url, json=data)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        ans = response.json()
        self.assertEqual(ans["result"][0], "Success")
        ans = ans["result"][1]["updated_order"]
        print(ans)
        self.assertEqual(ans["name"], "MyCoolOrder")
        self.assertEqual(ans["vk_group_id"], -33333)
        self.assertEqual(ans["interval"], 120)
        self.assertEqual(ans["left_days"], 50)
        self.assertEqual(ans["last_post_id"], 1000)
        url = f"{self.root}/orders/{id_}"
        # -----------get_order
        response = requests.get(url)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        ans = response.json()
        ans = ans["order"]
        self.assertEqual(ans["name"], "MyCoolOrder")
        self.assertEqual(ans["vk_group_id"], -33333)
        self.assertEqual(ans["interval"], 120)
        self.assertEqual(ans["left_days"], 50)
        self.assertEqual(ans["last_post_id"], 1000)
        # -----------get_order
        url = f"{self.root}/orders/by_name/MyCoolOrder"
        response = requests.get(url)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        ans = response.json()
        ans = ans["order"]
        self.assertEqual(ans["name"], "MyCoolOrder")
        self.assertEqual(ans["vk_group_id"], -33333)
        self.assertEqual(ans["interval"], 120)
        self.assertEqual(ans["left_days"], 50)
        self.assertEqual(ans["last_post_id"], 1000)
        # -----------
        url = f"{self.root}/users/by_tg/12345"
        response = requests.delete(url)
        self.assertEqual(response.status_code, 200)
        print(response.json())
        ans = response.json()
        self.assertEqual(ans["result"], "Success")

    def test3(self):
        url = f"{self.root}/users"
        data = {
            "tg_id": 12345
        }
        response = requests.post(url, json=data)
        # ----------
        url = f"{self.root}/orders"
        data = list()
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 400)
        # -------------
        data = dict()
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 400)
        # -------------
        data = {
            "user_tg_id": 12345,
            "name": "MyOrder",
            "vk_group_id": -22222,
            "interval": 60,
            "left_days": 100,
            "last_post_id": 123
        }
        response = requests.post(url, json=data)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        # -------------
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 413)
        # -------------
        data = {
            "user_tg_id": 12345,
            "name": "MyCoolOrder",
            "vk_group_id": -1,
            "interval": 1,
            "left_days": 1,
            "last_post_id": 1
        }
        response = requests.post(url, json=data)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        # -------------
        data = {
            "name": "MyCoolOrder",
            "vk_group_id": -33333,
            "interval": 120,
            "left_days": 50,
            "last_post_id": 1000
        }
        response = requests.put(url, json=data)
        # -------------
        url = f"{self.root}/orders/by_name/MyOrder"
        response = requests.delete(url)
        self.assertEqual(response.status_code, 200)
        print(response.json())
        ans = response.json()
        self.assertEqual(ans["result"], "Success")
        # --------------
        url = f"{self.root}/users/by_tg/12345"
        response = requests.delete(url)
        self.assertEqual(response.status_code, 200)
        print(response.json())
        ans = response.json()
        self.assertEqual(ans["result"], "Success")

    def test_all_users_get(self):
        url = f"{self.root}/users"
        response = requests.get(url)
        print("test_all_users_get")
        try:
            print(response.json())
        except:
            print(response)

    def test_user_delete(self):
        url = f"{self.root}/users/by_tg/12345"
        response = requests.delete(url)
        print("test_user_delete")
        try:
            print(response.json())
        except:
            print(response)

    def test_all_orders_get(self):
        url = f"{self.root}/orders"
        response = requests.get(url)
        print("test_all_orders_get")
        try:
            print(response.json())
        except:
            print(response)

    def test_order_delete(self):
        url = f"{self.root}/orders/1"
        response = requests.delete(url)
        print("test_user_delete")
        try:
            print(response.json())
        except:
            print(response)
