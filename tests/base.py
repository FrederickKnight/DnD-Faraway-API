import random
import uuid

class BaseTesting:
    def setup_class(self,endpoint,data):
        self.ENDPOINT = endpoint
        self.testing_data = data
    
    def test_add(self,client):
        _json,response = self.tst_add_data(client)
        
        self.tst_compare_data(_json,response,expect=True)


    def test_get_all(self,client):
        self.tst_get_all_data(client)
        
        
    def test_get_by_id(self,client):
        response_all = self.tst_get_all_data(client)
        res_all_index = self.get_random_select(response_all)
                
        _id = res_all_index["id"]
        response_by_id = client.get(f"{self.ENDPOINT}/{_id}")
        
        assert response_by_id.status_code == 200,"Response status should be 200"

        assert res_all_index == response_by_id.json["data"][0]
        
        
    def test_update(self,client):

        add_json,res_add_json = self.tst_add_data(client)
        
        self.tst_compare_data(add_json,res_add_json,expect=True)
        
        id_res_add_json = res_add_json["data"][0]["id"]
        
        to_update_json = self.get_json(self.testing_data,client)
        to_update_json["id"] = id_res_add_json
        
        # updated withoud id in url
        updated_response = client.put(f"{self.ENDPOINT}/update",json = to_update_json)
        
        assert updated_response.status_code == 200
        
        assert updated_response.json["data"][0] != res_add_json["data"][0]
        
        to_update_json_normalized_keys = self.get_normalice_keys(to_update_json)
        self.tst_compare_data(to_update_json_normalized_keys,updated_response.json,expect=True)
        
        
    def test_update_by_id(self,client):

        add_json,res_add_json = self.tst_add_data(client)
        
        self.tst_compare_data(add_json,res_add_json,expect=True)
        
        id_res_add_json = res_add_json["data"][0]["id"]
        
        to_update_json = self.get_json(self.testing_data,client)
        
        # updated withoud id in url
        updated_response = client.put(f"{self.ENDPOINT}/{id_res_add_json}/update",json = to_update_json)
        
        assert updated_response.status_code == 200
        
        assert updated_response.json["data"][0] != res_add_json["data"][0]
        
        to_update_json_normalized_keys = self.get_normalice_keys(to_update_json)
        self.tst_compare_data(to_update_json_normalized_keys,updated_response.json,expect=True)
        
        
    # Add Delete Test
    ##################
    #################3
    
    
    # helpers
    def get_json(self,_data:dict,client):   
        data = _data.copy()
        
        # optimize later
        for key in data:
            
            # check special id
            if isinstance(data[key],tuple):
                
                if "id_model_" in data[key][0]:
                    
                    unique_id_model = 1
                    
                    testing_data = self.get_json(data[key][1]().get_testing_data(),client)
                    endpoint = f"api/{data[key][0].split("id_model_")[1]}"
                    
                    res = client.post(f"{endpoint}/add",json = testing_data)
                    
                    if res.status_code == 200:
                        unique_id_model = res.json["data"][0]["id"]
                                          
                    data[key] = unique_id_model
                    
                    
            elif isinstance(data[key],str):
                
                if "id_model_" in data[key]:
                    
                    id_model = 0
                    
                    endpoint = f"api/{data[key].split("id_model_")[1]}"
                    res = client.get(f"{endpoint}/")
                    
                    if res.status_code == 200:
                        id_model = self.get_random_select(res.json)["id"]

                    data[key] = id_model
                        
                    
                if data[key] == "uuid":
                    data[key] = f"test_{key}_{uuid.uuid4()}"
                    
                if data[key] == "version":
                    numbers = [f"{random.randint(0,20)}" for _ in range(3)]
                    data[key] = "5."+".".join(numbers)
                    
                if data[key] == "bool":
                    data[key] = random.randint(0,1)
                    
                if data[key] == "int":
                    data[key] = random.randint(0,99)
                    
        return data
        
        
    def get_random_select(self,data):
        all_index = [d["id"] for d in data["data"]]
        selected_index = random.choice(all_index)
        return next((d for d in data["data"] if d["id"] == selected_index),None)
    
    def normalice(self,data):
        for key in self.testing_data:
            if self.testing_data[key] == "bool":
                data[key] = 1 if data[key] else 0
        return data
    
    
    def get_testing_data(self):
        return self.testing_data
    
    def get_normalice_dict(self,_json):
        
        for key in self.testing_data:
            if "id_" in key:
                normalice_key = key.split("id_")[1]
                _json[normalice_key] = _json[normalice_key]["id"]
                
        return _json
    
    def get_normalice_keys(self,_json):
        
        normalice_key = None
        for key in self.testing_data:
            if "id_" in key:
                temp_data = _json[key]
                normalice_key = key.split("id_")[1]
                
                del _json[key]
                _json[normalice_key] = temp_data
                
        return _json
    # repetitive tests
    
    def tst_get_all_data(self,client):
        response = client.get(f"{self.ENDPOINT}/")
        _json = response.json
        
        assert response.status_code == 200,"Response status should be 200"
        assert _json["metadata"]["size"] > 0,"Response should be more than 0"

        return _json
    

    def tst_add_data(self,client):
        """ Get entry Json and Response Data
        
        """
        _json = self.get_json(self.testing_data,client)
        
        _res = client.post(f"{self.ENDPOINT}/add",json = _json)
        res_json = _res.json
        
        assert _res.status_code == 200,"Response status should be 200"
        assert res_json["metadata"]["size"] == 1, "Json Size of Response should be 1"
        
        _json = self.get_normalice_keys(_json)
                
        return _json,res_json
    
    def tst_compare_data(self,entry_json,entry_response,expect:bool=True):
        _json = entry_json
        
        res_json = self.get_normalice_dict(self.normalice(entry_response["data"][0]))
        
        _json_keys = _json.keys()
        
        for key in _json_keys:
            if expect == True:
                assert _json[key] == res_json[key],f'Expect True for key "{key}"" in [{_json[key]}] and [{res_json[key]}]'
            
            elif expect == False:
                assert _json[key] != res_json[key],f'Expect False for key "{key}"" in [{_json[key]}] and [{res_json[key]}]'
                