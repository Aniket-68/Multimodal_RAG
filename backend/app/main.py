import fitz
document = fitz.open(r"D:\Github\Multimodal_RAG\backend\data\raw\Flat_303_Bhakti_Rajarshi_Reg_L&L_09_01_2027.pdf")
print("Number of pages:", document.page_count)

print(document.metadata)
page = document[0]
print("TEXT\n")
print(page.get_text("blocks"))
print("IMAGE LIST\n")
# print(page.get_text("json"))
# print(page.get_text("json"))