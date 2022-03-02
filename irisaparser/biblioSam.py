# import parser object from tike
from tika import parser  
  
# opening pdf file
parsed_pdf = parser.from_file("Torres-moreno1998.pdf")
  
data = parsed_pdf['content'] 
  
references1 = "REFERENCES"
references2 = "References"
if references1 in data:
    print('Word found1.') 
    integer = data.find(references1)
    print(data[integer+len(references1):])
elif references2 in data:
    integer = data.find(references2)
    print(data[integer+len(references1):])

else:
    print('There is no reference.') 



