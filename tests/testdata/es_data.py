from .common import get_list_unique_values_by_key


movies_data = [ {'_id': 'e7e6d147-cc10-406c-a7a2-5e0be2231327', 'id': 'e7e6d147-cc10-406c-a7a2-5e0be2231327', 'imdb_rating': 2.0, 'genres': [{'id': '1cacff68-643e-4ddd-8f57-84b62538081a', 'name': 'Drama'}, {'id': 'a886d0ec-c3f3-4b16-b973-dedcf5bfa395', 'name': 'Short'}], 'title': 'Shooting Star', 'description': 'How far would a mother go to protect her children?', 'director': ['Lyubo Yonchev'], 'actors_names': ['Eleni Dekidis', 'Kalia Kamenova', 'Lyudmil Hristov', 'Sevar Ivanov'], 'writers': [{'id': '178c9768-6d04-4419-8afc-83d8228421ef', 'name': 'Yassen Genadiev'}, {'id': '1b8773c9-7e15-4809-a6d7-949c9b9def3b', 'name': 'Lyubo Yonchev'}], 'writers_names': ['Lyubo Yonchev', 'Yassen Genadiev'], 'actors': [{'id': '224454bf-e018-4f06-8b1f-e32a6411558a', 'name': 'Kalia Kamenova'}, {'id': '290fe246-618d-445f-bce1-660d720b1ffa', 'name': 'Sevar Ivanov'}, {'id': 'bac1767f-12d0-4bae-a731-e555074cbe40', 'name': 'Eleni Dekidis'}, {'id': 'f3d972f2-03d1-49cb-ab70-ca32c1c09a28', 'name': 'Lyudmil Hristov'}]},
                {'_id': 'e7f32409-cc55-4af7-ad30-74558a904467', 'id': 'e7f32409-cc55-4af7-ad30-74558a904467', 'imdb_rating': 5.1, 'genres': [{'id': '526769d7-df18-4661-9aa6-49ed24e9dfd8', 'name': 'Thriller'}], 'title': 'Stalked by a Reality Star', 'description': 'A teenage girl lies about her age to get into a Hollywood party and meets a handsome reality TV star - but when she finds out he is a creep and rejects him, he becomes obsessed and starts ...', 'director': ['Robert Malenfant'], 'actors_names': ['Cynthia Preston', 'Emily Bader', 'Jordan Doww', 'Robert Scott Wilson'], 'writers': [{'id': '20f7f6d1-4e1c-4e73-b406-f01e222a4976', 'name': 'Ken Sanders'}, {'id': 'b758b4d3-730f-491a-aa71-3900e4bf1f6e', 'name': 'Aidan Scott'}], 'writers_names': ['Aidan Scott', 'Ken Sanders'], 'actors': [{'id': '5d14cb83-01cc-4581-82f5-4c99ec78cc05', 'name': 'Emily Bader'}, {'id': '6d77d1b0-49e0-4194-845a-25c3d0ffdcfc', 'name': 'Cynthia Preston'}, {'id': '74e6c1ec-416f-4e7e-b13f-a1e9ec000a4c', 'name': 'Jordan Doww'}, {'id': 'c5d2697b-dfa1-49c8-86d5-0452d6bb81a9', 'name': 'Robert Scott Wilson'}]},
                {'_id': 'e83a8d14-2ebf-4aa6-87b4-4cf2eae2840d', 'id': 'e83a8d14-2ebf-4aa6-87b4-4cf2eae2840d', 'imdb_rating': 5.0, 'genres': [{'id': '6a0a479b-cfec-41ac-b520-41b2b007b611', 'name': 'Animation'}, {'id': '5373d043-3f41-4ea8-9947-4b746c601bbd', 'name': 'Comedy'}, {'id': 'a886d0ec-c3f3-4b16-b973-dedcf5bfa395', 'name': 'Short'}], 'title': 'Star Wreck 2: The Old Shit', 'description': '', 'director': ['Samuli Torssonen'], 'actors_names': ['Janne Torssonen', 'Rudi Airisto', 'Samuli Torssonen'], 'writers': [{'id': '2ede5838-9b45-4ba0-a369-dc7acce459bc', 'name': 'Samuli Torssonen'}, {'id': 'ca2c7a3d-7583-4d57-80c2-ffc1a27282e5', 'name': 'Rudi Airisto'}], 'writers_names': ['Rudi Airisto', 'Samuli Torssonen'], 'actors': [{'id': '2ede5838-9b45-4ba0-a369-dc7acce459bc', 'name': 'Samuli Torssonen'}, {'id': 'bb619697-ec0e-45ff-97f3-864a450583a4', 'name': 'Janne Torssonen'}, {'id': 'ca2c7a3d-7583-4d57-80c2-ffc1a27282e5', 'name': 'Rudi Airisto'}]},
                {'_id': 'e891bebc-786c-4fe8-948e-c6d4007146f9', 'id': 'e891bebc-786c-4fe8-948e-c6d4007146f9', 'imdb_rating': 6.5, 'genres': [{'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff', 'name': 'Action'}, {'id': 'a886d0ec-c3f3-4b16-b973-dedcf5bfa395', 'name': 'Short'}, {'id': '6c162475-c7ed-4461-9184-001ef3d9f26e', 'name': 'Sci-Fi'}], 'title': 'Odyssey: A Star Wars Story', 'description': '', 'director': ['Mark Alex Vogt'], 'actors_names': ['Jason Louder', 'Katharina Daue', 'Michael Christopher Rodney', 'Mitchell Smalenski'], 'writers': [], 'writers_names': [], 'actors': [{'id': '331b4ae2-96da-44a1-94b4-ebf02e052ac6', 'name': 'Michael Christopher Rodney'}, {'id': '5bb9a3c5-c6ba-4627-ba6f-b5911f544f86', 'name': 'Jason Louder'}, {'id': 'ab93f5dd-b508-4457-8e2e-5e8ea70c6355', 'name': 'Katharina Daue'}, {'id': 'abefb3ba-2db1-436e-865e-536b2e5243ab', 'name': 'Mitchell Smalenski'}]},
                {'_id': 'e8c6825b-69f5-4aac-9960-23fa2b803339', 'id': 'e8c6825b-69f5-4aac-9960-23fa2b803339', 'imdb_rating': 7.8, 'genres': [{'id': '1cacff68-643e-4ddd-8f57-84b62538081a', 'name': 'Drama'}, {'id': 'b92ef010-5e4c-4fd0-99d6-41b6456272cd', 'name': 'Fantasy'}], 'title': 'Star Ocean: The Last Hope', 'description': '', 'director': ['Ayuki Katayama', 'Jonathan Klein', 'Kay Miura', 'Kimiko Kai', 'Koji Hayashi', 'Mitsuo Iwao', 'Toshiyuki Terada'], 'actors_names': ['Daisuke Kishio', 'Megumi Toyoguchi', 'Mitsuki Saiga', 'Miyuki Sawashiro'], 'writers': [{'id': '33c3b6ba-7435-4e70-a7be-431337a2c590', 'name': 'Gi Jin Jang'}, {'id': '529ca49d-05db-4afc-a29c-ce4279cae95c', 'name': 'Kazumasa Niitsuma'}, {'id': 'a105f73c-19ac-4979-a2f5-225b718527f4', 'name': 'Yutaka Saito'}], 'writers_names': ['Gi Jin Jang', 'Kazumasa Niitsuma', 'Yutaka Saito'], 'actors': [{'id': '1f5f7f56-3883-4d2e-abb8-98eee3e1b01c', 'name': 'Megumi Toyoguchi'}, {'id': '44c6ce45-3f19-4363-a65d-33de005fa303', 'name': 'Mitsuki Saiga'}, {'id': '50fa7d2f-c6a8-451a-986a-bc343106b775', 'name': 'Daisuke Kishio'}, {'id': 'd92e8b22-9f05-433e-ac13-d3b07c0821ae', 'name': 'Miyuki Sawashiro'}]},
                {'_id': 'e95044a7-1f66-4164-9650-3bf2132d7119', 'id': 'e95044a7-1f66-4164-9650-3bf2132d7119', 'imdb_rating': 5.8, 'genres': [{'id': '5373d043-3f41-4ea8-9947-4b746c601bbd', 'name': 'Comedy'}], 'title': 'The Young Comedians All-Star Reunion', 'description': 'Howie Mandel in Toronto, Steven Wright in Boston, Harry Anderson in Los Angeles, Richard Belzer in New York, and Robin Williams in San Fransisco (featured in the original "Young Comedian" TV specials) go back to where they started and showcase a new comedian.', 'director': ['Walter C. Miller'], 'actors_names': ['Barry Crimmins', 'Howard Busgang', 'Howie Mandel', 'Steven Wright'], 'writers': [{'id': '42bc6979-f4c6-49dc-bdc2-ea6696bb6792', 'name': 'Rick Mitz'}], 'writers_names': ['Rick Mitz'], 'actors': [{'id': '07a54e6c-57ec-4f68-8561-be3abfe2b29a', 'name': 'Steven Wright'}, {'id': '1071dc2b-0fd6-40be-9672-ef62297f2383', 'name': 'Howie Mandel'}, {'id': '18b1fc7d-fc82-4a87-9c11-b90e3607cf6c', 'name': 'Howard Busgang'}]}]


persons_data = [
    {
        '_id': person['id'],
        **person
    }
    for person in get_list_unique_values_by_key(movies_data, 'actors')
]


genres_data = [
    {
        '_id': genre['id'],
        **genre
    }
    for genre in get_list_unique_values_by_key(movies_data, 'genres')
]
