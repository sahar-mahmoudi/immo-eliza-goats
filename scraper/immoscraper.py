
    
    
# def get_(self) -> None:
#     """
#     Retrieve the features of each propertie
#     """
#     #for property in self.properties:
#     #endpoint =
#     response = self.session.get(self.root_url )
#     features = response.json()

#     self.leaders_data[country] = [
#         {
#             "first_name": leader["first_name"],
#             "last_name": leader["last_name"],
#             "id": leader["id"],
#             "birth_date": leader["birth_date"],
#             "death_date": leader["death_date"],
#             "place_of_birth": leader["place_of_birth"],
#             "start_mandate": leader["start_mandate"],
#             "end_mandate": leader["end_mandate"],
#             "url": leader["wikipedia_url"],
#             "first_paragraph": self.get_first_paragraph(leader["wikipedia_url"])
#         } for leader in all_leaders
#     ]