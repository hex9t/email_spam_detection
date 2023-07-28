import streamlit as st
from PIL import Image
import pytesseract
from spam_detection import spam_detection
from email_system import get_text_plain_part
from email_system import format_email_headers
from email_system import read_email_content_by_uid
from email_system import get_last_email_uid
from email_system import delete_email_by_uid
import re
import time

def read_variables_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    variable_dict = {}
    for line in lines:
        parts = line.strip().split("=")
        if len(parts) == 2:
            name = parts[0].strip()
            value = int(parts[1].strip())
            variable_dict[name] = value

    return variable_dict

def write_variables_to_file(file_path, variable_dict):
    with open(file_path, 'w') as file:
        for name, value in variable_dict.items():
            file.write(f"{name} = {value}\n")

def init_session_state():
    if 'number_of_users' not in st.session_state:
        st.session_state.number_of_users = 0

# Function to increment number_of_users by 1 when the 'OK' button is clicked
def increment_users():
    st.session_state.number_of_users += 1



def extract_money_sentences(text):
    # Define the regex pattern to match money values
    pattern = r'\$\s?\d+(?:,\d{3})*(?:\.\d{2})?'

    # Find all occurrences of the pattern in the text
    money_sentences = re.findall(pattern, text)

    if not money_sentences:
        return None
    else:
        return money_sentences

def find_words_in_string(input_string):
    words_to_find = ["mother", "father", "uncle", "son", "brother"]
    found_words = []

    for word in words_to_find:
        if word in input_string.lower():
            found_words.append(word)

    return found_words

# Example usage:
input_string = "My mother is a doctor, and my father works in the city. I have a younger brother."
result = find_words_in_string(input_string)

print("Found words:", result)


def extract_links(text):
    # Define the regex pattern to match URLs
    pattern = r'https?://\S+|www\.\S+'

    # Find all occurrences of the pattern in the text
    links = re.findall(pattern, text)

    if not links:  # If links list is empty
        return None  # You can also return False, an empty list, or any other custom value
    else:
        return links



def get_color(score):
    if 6<=score <=10:
        # Calculate the RGB values for red color (255, 0, 0)
        color_hex = "#FF0000"
    elif 3<=score < 6:
        # Calculate the RGB values for orange color (255, 165, 0)
        color_hex = "#FFA500"
    else:
        # Calculate the RGB values for green color (0, 128, 0)
        color_hex = "#008000"

    return color_hex
def risk(text):
    counter = [0,0] 
    text_v=text.split()
    for word in text_v:
        if spam_detection(word)==1:
            counter[0] = counter[0] + 1 
        elif spam_detection(word)==0 : 
            counter[1] = counter[1] + 1   
    medium = round(counter[0]/len(text_v) * 10,2 )
    return medium   
        

def highlight_spam_words(text):
    words = text.split()
    highlighted_text = ""

    for word in words:
        if spam_detection(word):
            highlighted_text += f'<span style="color:red">{word}</span> '
        else:
            highlighted_text += f"{word} "

    return highlighted_text.strip()


def advanced(text):
    score = risk(text)
                  
    if extract_links(text)==None:
        st.write("no links...")
    else:
        st.warning(f"the email provided a link: {extract_links(text)}")   
        score +=1   
    if extract_money_sentences(text)==None:
        st.write("no money is mentionned")
    else:
        st.warning(f"money declared:{extract_money_sentences(text)}")
        score +=1
    if find_words_in_string(text)==[]:
        st.write("no family mentionned")
    else:
        st.warning(f"family members who got mentionned: {find_words_in_string(text)}")  
        score +=len(find_words_in_string(text))
    color = get_color(score)
    st.markdown(f'<h1 style="color: {color}; font-size: 48px; text-align: center;">Score: {score}/10</h1>', unsafe_allow_html=True)
    if 6<=score <=10:
        st.write("this is still too suspicious be aware !")
    if 3<= score <6:
        st.write("this is a bit suspicious so be aware !")
    elif score < 3 :
        st.write("it looks like this email is safe")                  


    
    






def design():
    # Custom CSS styling
    st.markdown(
        """
        <style>
            body {
                background-color: #1F1F1F;
                color: #FFFFFF;
                font-family: 'Helvetica', Arial, sans-serif;
            }
            .main {
                background-color: #2A2A2A;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* Add a subtle box-shadow effect */
                max-width: 800px;
                margin: 0 auto; /* Center the container horizontally */
                margin-top: 100px; /* Add some top margin for spacing */
            }
            .title {
                font-size: 48px;
                font-weight: bold;
                margin-bottom: 20px;
                color: #FF5722; /* Use a vibrant color for the title */
            }
            .subtitle {
                font-size: 24px;
                margin-bottom: 30px;
                color: #FF7043; /* Use a different color for the subtitle */
            }
            .feature {
                font-size: 18px;
                margin-bottom: 15px;
            }
            .action-button {
                background-color: #FF5722;
                color: #FFFFFF;
                padding: 12px 24px;
                border: none;
                border-radius: 5px;
                font-size: 20px;
                cursor: pointer;
            }
            .action-button:hover {
                background-color: #FF7043;
            }
            .image-container {
                text-align: center; /* Center the image */
                margin-bottom: 20px;
            }
            .image-caption {
                font-size: 14px;
                color: #A0A0A0; /* Use a lighter color for the caption */
            }
            /* Add shine effect to the edges */
            .main::before {
                content: "";
                position: absolute;
                top: -5px;
                right: -5px;
                bottom: -5px;
                left: -5px;
                z-index: -1;
                background: linear-gradient(
                    to right bottom,
                    rgba(255, 255, 255, 0.1),
                    rgba(255, 255, 255, 0.05)
                );
                border-radius: 15px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


    # Add an image
    st.image("https://www.k12prospects.com/wp-content/uploads/2018/11/top-image-without-frame-Avoiding-Email-Spam-Filters.jpg", use_column_width=True)

    st.markdown("<div class='title'>Welcome to The HOMEPAGE</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>use my app but with care please :)</div>", unsafe_allow_html=True)

    # Cool features section
    st.markdown("<div class='feature'>", unsafe_allow_html=True)
    st.markdown("## spam detection ")
    file_path = 'number_of_users.txt'
    dict=read_variables_from_file(file_path)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Uses", value=dict['number_of_uses'], delta="Total Uses")
    with col2:
        st.metric(label="Spam Detections", value=dict['detection_times'], delta="New Detections")
    with col3:
        st.metric(label="Safe Emails", value=dict['safe_emails'], delta="New Safe Emails")

    

   
    
    
    
    # Close the main content section
    st.markdown("</div>", unsafe_allow_html=True)
# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image):
    # Convert the image to grayscale
    image = image.convert("L")

    # Use Tesseract to perform OCR and extract text
    text = pytesseract.image_to_string(image)

    # Return the extracted text
    return text

def main():
    file_path = 'number_of_users.txt'
    variable_dict = read_variables_from_file(file_path)
    st.set_page_config(page_title="Image Text Extraction and Spam Detection", layout="wide")

    # Set app title and header
    st.title("Image Text Extraction and Spam Detection")
    st.markdown("This is a project of mine to extract text from images and detect spam emails.")

    # Create a sidebar
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio(
        "Select an option:",
        ["💒:Home Page","📜:Text Input", "🖼️ :Image Upload", "📬:Gmail Spam Scan"]
    )

    # Text Input mode



    if app_mode == "📜:Text Input":
        st.header("Text Input")
        st.subheader("Enter your text:")

        his_email = st.text_area("Enter your email:")

        if st.button("Submit Your Email"):
        
  
            prediction = spam_detection(his_email)
            if prediction == 1:
                st.warning("The text is classified as spam.")
            elif prediction == 0:
                st.success("The text is not classified as spam.")
                advanced(his_email)


    elif app_mode == "💒:Home Page":
        design()
        
        

        
        
           

    # Gmail Spam Scan mode
    elif app_mode == "📬:Gmail Spam Scan":
        st.header("Gmail Spam Scan")
        st.subheader("Enter your Gmail credentials:")

        username = st.text_input("Username (Gmail email)")
        password = st.text_input("Password", type="password")
        imap_server = 'imap.gmail.com'

        if st.button("Analyze Gmail Inbox"):
            
            increment_users()
            last_email_uid = get_last_email_uid(imap_server, username, password)
            if last_email_uid:
                st.write("Latest Email Content:")
                input = read_email_content_by_uid(imap_server, username, password, last_email_uid)
                st.code(input, language="plaintext")
                
                prediction = spam_detection(input)
                if prediction == 1:
                    st.error("The email is classified as spam.")
                    st.warning("The email has been deleted from your inbox.")
                    delete_email_by_uid(imap_server, username, password, last_email_uid)
                else:
                    st.success("The email is not classified as spam.")
                    advanced(input)
            else:
                st.error("No emails found in the mailbox.")
        


                
            

            


                     
                  
             
             

    # Image Upload mode
    elif app_mode == "🖼️ :Image Upload":
        st.header("Image Upload")
        st.subheader("Upload an image:")
        uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

        if st.button("Process Image") and uploaded_image is not None:
            variable_dict["number_of_uses"] +=1
            write_variables_to_file(file_path, variable_dict)
            image = Image.open(uploaded_image)
            extracted_text = extract_text_from_image(image)

            st.write("Checking for spam...")
            prediction = spam_detection(extracted_text)

            if prediction == 1:
                st.warning("The extracted text is classified as spam.")
                variable_dict["detection_times"]+=1
                write_variables_to_file(file_path, variable_dict)
                
            elif prediction == 0:
                st.success("The extracted text is not classified as spam.")
                with st.spinner("Running advanced scanning..."):
                 advanced(extracted_text)
                 highlighted_text = highlight_spam_words(extracted_text)
                 st.write("words we find suspicious in your email such dates, threatening messages...etc:")

                 st.markdown(highlighted_text, unsafe_allow_html=True)
                 variable_dict["safe_emails"]+=1
                 write_variables_to_file(file_path, variable_dict)
                 
                                

   
         
                


    # Display the score with colored background

                        
              
             
      

if __name__ == "__main__":
    main()

