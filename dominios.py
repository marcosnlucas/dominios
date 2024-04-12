import whois # 👉️ Import whois module

dm_info =  whois.whois("hackernoon.com") # 👉️ Get Domain Info

print(dm_info)

print("Registar:", dm_info.registrar) # 👉️ Get Registar

print("Creation Date:", dm_info.creation_date) # 👉️ Get Creation Date

print("Expiration Date:", dm_info.expiration_date) # 👉️ Expiration Date

print("Country:", dm_info.country) # 👉️ Get Country
