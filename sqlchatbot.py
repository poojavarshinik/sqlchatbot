import os
import time
import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Set the API key environment variable
os.environ["GEMINI_API_KEY"] = "AIzaSyA0Jx5lovrPEfz7_4_fLFwP4vttlOuRmXc"  # Replace with your actual API key

# Configure the Google AI API with the API key from the environment variable
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    try:
        file = genai.upload_file(path, mime_type=mime_type)
        return file
    except exceptions.GoogleAPIError as e:
        st.error(f"An error occurred while uploading the file: {e}")
        raise

def wait_for_files_active(files):
    """Waits for the given files to be active."""
    for name in (file.name for file in files):
        try:
            file = genai.get_file(name)
            while file.state.name == "PROCESSING":
                time.sleep(10)
                file = genai.get_file(name)
            if file.state.name != "ACTIVE":
                raise Exception(f"File {file.name} failed to process")
        except exceptions.GoogleAPIError as e:
            st.error(f"An error occurred while checking file status: {e}")
            raise

def main():
    st.title("SQL Query Generator Chatbot")
    st.write("This chatbot generates SQL queries based on your natural language input.")

    # Path to the file to be uploaded
    file_path = "v3 keyword subindustry industry sector.csv"  # Update with the correct path

    # Upload file to Gemini
   
    try:
        files = [upload_to_gemini(file_path, mime_type="text/csv")]
       
    except Exception as e:
        st.error(f"Failed to upload file: {e}")
        return

    # Wait for the file to be active
   
    try:
        wait_for_files_active(files)
       
    except Exception as e:
        st.error(f"Failed to wait for file: {e}")
        return

    # Create the model with your generation configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        },
          system_instruction="you are now my SQL generator\nI will give you some natural language inputs, based on the inputs you have to generate me the sql queries\ni have two tables in my data base named \"infy_prod.infynd_uk_product_company\" and  \"infy_prod.infynd_uk_product_people\"\nSCHEMA FOR infy_prod.infynd_uk_product_company:\nid int NO PRI auto_increment [unique id for each column]\ncid int YES MUL [company id]\nAKEY int NO UNI [distinct id]\ncompany_registration_number varchar(50) YES MUL [company's registration number]\ncompany_registration_number_1 int YES [if the company's registration number is available this column will take the value 1 else it would take 0]\ncompany_permalink text YES [this is basically the concatenation of company name and cid]\nCompanyName varchar(256) YES MUL [name of the company]\nRegisterName varchar(256) YES MUL [company's registered name]\nAddress_Line_1 text YES [address]\nAddress_Line_2 text YES [address]\nAddress_Line_3 text YES [address]\nPost_Town varchar(128) YES MUL [post town]\nCounty varchar(128) YES [county]\nPost_Code varchar(50) YES MUL [post code]\nPost_Code_1 varchar(50) YES MUL [post code]\nCountry varchar(128) YES MUL [country]\nRegion varchar(128) YES MUL [region]\nhead_office_country varchar(255) YES MUL [this column tells in which country the head office of the company is located]\nlocation_type varchar(50) YES MUL [this tells if the company's location is a branch, head office, or single site]\ncompany_status varchar(255) YES MUL [this tells if the company is active, in administration, dissolved, liquidation, etc.]\naccount_categoy varchar(255) YES MUL [this tells about the account category (for example: full, small, group, etc.)]\nphone varchar(600) YES MUL [phone number]\nphone_1 varchar(600) YES [alternate phone number]\nphone_flag int YES MUL [if the company's phone number is available this column will take the value 1 else it would take 0]\ncompany_email varchar(600) YES MUL [email of the company]\ncompany_email_1 varchar(600) YES [alternate email of the company]\ncompany_email_flag int YES MUL [if the company's email is available this column will take the value 1 else it would take 0]\nwebsite varchar(256) YES MUL [website link of the company]\nwebsite_1 int YES [if the company's website link is available this column will take the value 1 else it would take 0]\nlinkedin varchar(600) YES MUL [linkedin link]\nlinkedin_1 int YES [if the company's linkedin is available this column will take the value 1 else it would take 0]\nfacebook varchar(256) YES [facebook link]\nfacebook_1 int YES [if the company's facebook link is available this column will take the value 1 else it would take 0]\ntwitter varchar(256) YES [twitter link]\ntwitter_1 int YES [if the company's twitter link is available this column will take the value 1 else it would take 0]\ninstagram varchar(256) YES [instagram link]\ninstagram_1 int YES [if the company's instagram link is available this column will take the value 1 else it would take 0]\nyoutube varchar(256) YES [youtube link]\nblog varchar(256) YES [blog link]\nemployees int YES MUL [number of employees in the company]\nemployee_range varchar(60) YES MUL [range of the employees count]\nturnover bigint YES MUL [turnover of the company]\nturnover_range varchar(128) YES MUL [turnover range of the company]\ncompany_type varchar(256) YES MUL [tells the type of the company (Limited Liability Partnership, PRI/LBG/NSC (Private, Limited by guarantee, no share capital, use of 'Limited' exemption), Private Limited Company)]\nfounded_date varchar(256) YES MUL [founded date of the company]\ncompany_age int YES MUL [age of the company]\nsic_code_all varchar(128) YES MUL [this column tells all the available standard industrial classification (SIC) codes]\nsic_text_all text YES MUL\nsic_code1 varchar(50) YES MUL [standard industrial classification (SIC) code]\nsic_code2 varchar(500) YES [standard industrial classification (SIC) code if more than one is available]\nsic_code3 varchar(500) YES [standard industrial classification (SIC) code if more than one is available]\nsic_code4 varchar(500) YES [standard industrial classification (SIC) code if more than one is available]\nsic_code varchar(50) YES [final standard industrial classification (SIC) code]\nsector_id int YES MUL [id of the sector to which the company belongs]\nindustry_id int YES MUL [id of the industry to which the company belongs]\nsub_industry_id int YES MUL [id of the subindustry to which the company belongs]\nsector varchar(512) YES MUL [sector to which the company belongs]\nindustry varchar(512) YES MUL [industry to which the company belongs]\nsub_industry varchar(600) YES MUL [subindustry to which the company belongs]\ntps varchar(256) YES\nctps varchar(256) YES MUL\nctps_1 int YES MUL\nQC_score int YES MUL\nQC_in_date date YES\nCRN_scoring int YES MUL\nAddress_scoring int YES MUL\nSector_scoring int YES MUL\nCompany_email_scoring int YES MUL\nSocial_handles_scoring int YES MUL\nPeople_association_scoring int YES MUL\nPhone_scoring int YES MUL\nothers_scoring int YES MUL\ncompany_score decimal(4,2) YES MUL\npeople_count bigint YES MUL\nTags text YES\ncompany_source varchar(256) YES MUL\ncompany_rank int YES MUL\nlogo_url text YES\nelastic_flag int YES MUL\nindex_flag varchar(128) YES MUL\nexclude_flag int YES MUL\nCompanyName_normalised varchar(256) YES MUL [cleaned and normalized final company name]\nRegisterName_normalised varchar(256) YES MUL [cleaned and normalized final company's registered name]\nflag1 int YES MUL\nflag2 varchar(60) YES MUL\nflag3 varchar(60) YES MUL\nflag4 int YES\nflag5 int YES\n\nSHEMA FOR infy_prod.infynd_uk_product_people\nid int NO PRI auto_increment [unique id for each column]\nAKEY int YES MUL [distinct id]\npeople_permalink varchar(256) YES [this is basically the concatenation of person name and pid]\npid int NO UNI [people id]\ntitle varchar(100) YES MUL [title of the person (MR, MRS, DR, etc.)]\nfirst_name varchar(128) YES MUL [first name of the person]\nmiddle_name varchar(128) YES MUL [middle name of the person]\nlast_name varchar(128) YES MUL [last name of the person]\njob_title varchar(128) YES MUL [job title of the person]\nPersonLinkedin varchar(258) YES MUL [personal linkedin profile link]\npeople_email varchar(128) YES MUL [email of the person]\npeople_email_1 varchar(128) YES MUL [alternate email of the person]\npeople_email_flag int YES MUL [if the person's email is available this column will take the value 1 else it would take 0]\npeople_email_score int YES MUL\npp_process_date date YES\npeople_QC_score int YES MUL\npeople_QC_in_date date YES\npeople_score int YES MUL\nskill text YES MUL [skills of the person]\npeople_town varchar(128) YES MUL [town of the person's location]\npeople_country varchar(128) YES MUL [country of the person's location]\npeople_postcode varchar(128) YES MUL [postcode of the person's location]\njob_title_level varchar(60) YES MUL [level of the job title (manager, senior, unclassified, director)]\npeople_rank int YES MUL\npeople_source varchar(100) YES MUL\npeople_logo text YES\npsc varchar(1) YES MUL\noccupation varchar(128) YES MUL\nperson_number varchar(128) YES MUL\nceased_on date YES MUL\nelastic_flag int YES MUL\nindex_flag varchar(128) YES MUL\nexclude_flag int YES MUL\nukph_flag int YES MUL\nflag1 int YES MUL\nflag2 varchar(60) YES MUL\nflag3 varchar(60) YES MUL\nflag4 int YES MUL\nflag5 int YES MUL\nYour task is to generate an accurate SQL query to retrieve relevant data from the table based on the input. Begin by analyzing the input to identify the required data and context, then match the identified values or attributes to the corresponding schema columns.Iwill be providing you files for some columns alone. Refer to the provided files for column values; \nInstructions when dealing with company table:\nWhen handling the industry, sub_industry, and sector columns in the company table, the process should reference the provided file, which contains four columns: sector, industry, sub_industry, and keyword. Remember that the \"keyword\" column in the table is just for the reference. It is not a seperate column in any of the table.It si provided just for the matching process.The matching process should be conducted as follows:\n\n1.Sector Matching: Begin by attempting to match the input with the sector column in the file. If a match is found, return the corresponding sector\n\n2.Industry Matching: If no match is found in the sector column, proceed to the industry column. Search for a relevant match in the industry column and return the corresponding industry\n\n3.Sub-industry Matching: If no match is found in the industry column, move to the sub_industry column and look for a match. If a matching sub_industry is found, return it as the final output.\n\n4. Keyword Matching: If no matches are found in the sector, industry, or sub_industry columns, proceed to the keyword column. Search for any matching keyword within this column. If a match is found, determine the corresponding sub_industry associated with the matched keyword and return this sub_industry.\n\nImportant Note: Ensure that only values for sector, industry, and sub_industry that are present in the provided file are returned.Do not assume any industry\n For example, if the input is \"Helicopter tour agency,\" begin by searching in the sector column. If no match is found, move on to the industry column, followed by the sub_industry column. If no match is found in these columns, search the keyword column. Upon finding a matching keyword, return the corresponding sub_industry (in this case, \"Air Charter\"). The final output would be \"Air Charter.\"\n Example 2: if the input is \"construction\" begin by searching in the sector column. match is found for this, so the final output is \"construction\"\nwhen you dont find exact match but more relavent match you can use \"like\" conditions.When you find more relavent  column values, you can use like condition with a certain specifiv keyword\n\nWhen the user asks any specific SIC code then you have to check if it available in sic_code1, sic_code2 ,sic_code3 ,sic_code4\nWhile generating queries for company table , the select statement must select the following columns: akey,company_registration_number ,CompanyName ,Address_Line_1 ,Address_Line_2 ,Address_Line_3 ,Post_Town ,County ,Post_Code ,phone as 'db_phone',website ,linkedin ,facebook ,twitter ,sic_code_all ,sic_text_all ,sub_industry_1 ,industry_1 ,employees ,employee_range ,turnover ,turnover_range.\nif the user gives location values as UK or United Kingdom you need to add a condition which is\"Country in ('England','England/Wales','Scotland','Scotland/England','United Kingdom','Wales','Wales/England','Northern Ireland')\"\nInstructions when dealing with people table:\nWhen generating queries from peoplw table, the select statement must select the following columns: pid,title,first_name as 'f_name',last_name as 'l_name',job_title as 'job_people',job_title_level,people_email,people_email_score,PersonLinkedin.\nIf the user asks to give \"SDM job title levels\" you have to add a condition which is \"job_title_level in ('Director','senior','C level','VP_level','Company Secretary')\"\nWhen the user asks any specific job related queries , go with like condition and use job_title column\nWhen the user asks to give only valid records then the condition will be \"people_email_score>=83\". If they dont mention any condittion you need noe add this condition.\nEnsure the resulting SQL query accurately reflects the column names in the schema. And also if you are retrieving any column names from the files uploaded make sure to give the exact column names do not give me any description give only the query.\ni dont need any description, give me only sql query\nI want you to add \"excluse_flag=0\" as a basic condition at the end of every query for both the tables as a base conditions.\nwhen the user asks from both the table match it accordingly based on the user reqiurements by using joins on akey",

    )

    # Start a chat session with files included in the history

    chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        files[0],
        "i need business,photograph and car related companies  and their valid people who have email and  and are managers",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```sql\nSELECT \n    c.akey, \n    c.company_registration_number, \n    c.CompanyName, \n    c.Address_Line_1, \n    c.Address_Line_2, \n    c.Address_Line_3, \n    c.Post_Town, \n    c.County, \n    c.Post_Code, \n    c.phone AS 'db_phone', \n    c.website, \n    c.linkedin, \n    c.facebook, \n    c.twitter, \n    c.sic_code_all, \n    c.sic_text_all, \n    c.sub_industry_1, \n    c.industry_1, \n    c.employees, \n    c.employee_range, \n    c.turnover, \n    c.turnover_range,\n    p.pid, \n    p.title, \n    p.first_name AS 'f_name', \n    p.last_name AS 'l_name', \n    p.job_title AS 'job_people', \n    p.job_title_level, \n    p.people_email, \n    p.people_email_score, \n    p.PersonLinkedin\nFROM \n    infy_prod.infynd_uk_product_company c\nJOIN \n    infy_prod.infynd_uk_product_people p ON c.akey = p.akey\nWHERE \n    (\n        c.industry IN ('Business Consulting and Services', 'Photography', 'Retail Motor Vehicles')\n        OR c.sub_industry IN ('Business & Sales Development', 'Business & Trade Organisations', 'Business Advisory', 'Business Broker, Transfer Agent', 'Business Centres', 'Business Development', 'Business Information Services', 'Business Intelligence', 'Business Management Consultants', 'Business Services', 'Business Support', 'Commercial Photographer, Advertising Photography', 'Car Dealers', 'Car & Truck Fleet Leasing & Management', 'Car & Truck Leasing & Contract Hire', 'Car Accessories - Manufacturers & Suppliers', 'Car Auctions', 'Car Body Repairs', 'Car Breakdown & Recovery Services, Towing Services', 'Car Breakers & Dismantlers', 'Car Components & Parts Manufacturers', 'Car Credit & Finance', 'Car Customisation & Conversion Specialists', 'Car Audio & Entertainment Systems', 'Car Paint, Lacquer Manufacturers & Suppliers', 'Car Painters & Sprayers', 'Car Parking & Garaging', 'Car Parts', 'Car Radiator Servicing & Repairs', 'Car Rental', 'Car Sales', 'Car Supermarkets', 'Car Transportation', 'Car Trimmers & Upholsterers', 'Car Valeting', 'Car Washing & Polishing Equipment & Supplies', 'Car Window Tinting', 'Caravan & Recreational Vehicle Rental Agencies', 'Caravan Accessories & Supplies', 'Caravan Dealers & Manufacturers', 'Caravan Transport & Towing Services', 'Caravan/rv Parks', 'Caravans - Servicing & Repairs', 'Classic Car Specialists', 'Commercial Vehicle Bodybuilders & Repairers', 'Commercial Vehicle Breakdown & Recovery Services', 'Commercial Vehicle Component Manufacturers', 'Commercial Vehicle Dealers', 'Commercial Vehicle Security And Alarms', 'Commercial Vehicle Servicing, Repairs, Parts & Accessories', 'Motor Cycle Breakers & Dismantlers', 'Motor Cycle Repairs Garages, Shops', 'Motorcycle & Parts, Component Manufacturers', 'Motorcycle Clothing & Accessories', 'Motorcycle Parts & Accessories', 'Motorcycle Training/driving Schools', 'Motorcycles & Scooters', 'Motor Factors', 'Motoring Organisations', 'New & Used Car Sales', 'New & Used Spare Parts', 'New & Used Vehicle Sales', 'Van & Truck Hire/rental', 'Vehicle Auctions', 'Vehicle Electronics & Electrical Systems', 'Vehicle Escorts', 'Vehicle Fleet Management Consultants', 'Vehicle Flooring & Vehicle Acoustics', 'Vehicle Glass Repair & Replacement & Adas Calibration', 'Vehicle Hire', 'Vehicle Inspection Services', 'Vehicle Movements & Transport', 'Vehicle Salvage & Vehicle Breaking', 'Vehicle Signage', 'Vehicle Tracking System/gps Suppliers'\n    )\n  AND p.job_title_level = 'Manager'\n  AND p.people_email_flag = 1\n  AND p.people_email_score >= 83\n  AND c.exclude_flag = 0\n  AND p.exclude_flag = 0;\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "give me beauty,sports,transport and airline companies that are located in cambridge with employees more than 1000 and revenue more than 900k and also give me people who work there as a administrator or human resource and have valid email",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```sql\nSELECT \n    c.akey, \n    c.company_registration_number, \n    c.CompanyName, \n    c.Address_Line_1, \n    c.Address_Line_2, \n    c.Address_Line_3, \n    c.Post_Town, \n    c.County, \n    c.Post_Code, \n    c.phone AS 'db_phone', \n    c.website, \n    c.linkedin, \n    c.facebook, \n    c.twitter, \n    c.sic_code_all, \n    c.sic_text_all, \n    c.sub_industry_1, \n    c.industry_1, \n    c.employees, \n    c.employee_range, \n    c.turnover, \n    c.turnover_range,\n    p.pid, \n    p.title, \n    p.first_name AS 'f_name', \n    p.last_name AS 'l_name', \n    p.job_title AS 'job_people', \n    p.job_title_level, \n    p.people_email, \n    p.people_email_score, \n    p.PersonLinkedin\nFROM \n    infy_prod.infynd_uk_product_company c\nJOIN \n    infy_prod.infynd_uk_product_people p ON c.akey = p.akey\nWHERE \n    (\n        c.industry IN ('Performing Arts and Spectator Sports', 'Freight and Package Transportation', 'Airlines and Aviation')\n        OR c.sub_industry IN ('Beauty & Spas', 'Sports & Leisure Activities Schools', 'Sports Clubs & Associations', 'Sports Equipment Manufacturers & Distributors', 'Sports Grounds & Stadium Contractor', 'Sports Grounds & Stadiums', 'Sports Injury Clinics', 'Sports Management & Promotion', 'Sports Nutrition Supplements', 'Public Swimming Pools', 'Skating Rinks', 'Golf Courses & Clubs', 'Golf Driving Ranges', 'Golf Equipment & Supplies',  'Health Clubs, Gymnasiums & Beauty Centres', 'Watersports', 'Sailing Schools', 'Horse Drawn Vehicles - Hire', 'Horse Livery', 'Horse Trainers', 'Cycling', 'Exercise & Workout/fitness Classes', 'Bungee Jumping', 'Discos', 'Bowling Alleys', 'Bouncy Castles & Inflatables Hire',  'Combat Games/fighting Games', 'Paintball Games', 'Paintball Suppliers', 'Racecourses & Tracks', 'Squash Courts', 'Stage Lighting', 'Skates & Skateboarding', 'Air & Ocean Freight Forwarding', 'Airport Transfers', 'Bus & Coach Operators & Stations', 'Coach Hire', 'Driver Hire', 'Driver Training & Transport Management Training', 'Driving Schools/ Motor Training Schools', 'Executive Chauffeur Service', 'Freight Service', 'General Haulage & Heavy Haulage', 'Heavy Lift & Oversized Cargo Management', 'Logistics', 'Mini Bus Hire', 'Mini Bus Self Drive Hire/rental', 'Motor Cycle Hire', 'Rail & Road Haulage Services', 'Road Haulage', 'Road Construction Service Contractors', 'Road Marking & Surfacing Equipment & Material Manufacturers', 'Trailer Rental Services', 'Trailers & Towing Equipment', 'Transporting Horses', 'Transporting Of Computer Equipment', 'Trucking logistics', 'Truck Transportation', 'Towing', 'Ridesharing', 'Airline Services', 'Aircraft Charter & Rental Service', 'Aircraft Services', 'Aircraft Charter' \n    )\n    AND c.Post_Town = 'Cambridge' \n    AND c.employees > 1000 \n    AND c.turnover > 900000\n    AND (\n        p.job_title LIKE '%Administrator%'\n        OR p.job_title LIKE '%Human Resources%'\n    )\n    AND p.people_email_flag = 1\n    AND p.people_email_score >= 83\n    AND c.exclude_flag = 0\n    AND p.exclude_flag = 0;\n```\n\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "tropical fish store companies in luton that with more than 100 employees and with revenue of 800k ",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```sql\nSELECT \n    akey,\n    company_registration_number,\n    CompanyName,\n    Address_Line_1,\n    Address_Line_2,\n    Address_Line_3,\n    Post_Town,\n    County,\n    Post_Code,\n    phone AS 'db_phone',\n    website,\n    linkedin,\n    facebook,\n    twitter,\n    sic_code_all,\n    sic_text_all,\n    sub_industry,\n    industry,\n    employees,\n    employee_range,\n    turnover,\n    turnover_range\nFROM\n    infy_prod.infynd_uk_product_company\nWHERE \n    sub_industry = 'Pet Shops & Pet Supplies' AND Post_Town = 'Luton' AND employees > 100 AND turnover > 800000\n    AND exclude_flag = 0;\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "give me it related companies and accident repair companies in avon",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```sql\nSELECT \n    akey,\n    company_registration_number,\n    CompanyName,\n    Address_Line_1,\n    Address_Line_2,\n    Address_Line_3,\n    Post_Town,\n    County,\n    Post_Code,\n    phone AS 'db_phone',\n    website,\n    linkedin,\n    facebook,\n    twitter,\n    sic_code_all,\n    sic_text_all,\n    sub_industry,\n    industry,\n    employees,\n    employee_range,\n    turnover,\n    turnover_range\nFROM\n    infy_prod.infynd_uk_product_company\nWHERE \n    (\n        industry = 'IT Services and IT Consulting'\n        OR sub_industry = 'Accident Management'\n    )\n    AND County = 'Avon'\n    AND exclude_flag = 0;\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "give me agricultural industries that are in england and  give me the people who are in decision making level\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```sql\nSELECT c.akey, c.company_registration_number, c.CompanyName, c.Address_Line_1, c.Address_Line_2, c.Address_Line_3, c.Post_Town, c.County, c.Post_Code, c.phone AS 'db_phone', c.website, c.linkedin, c.facebook, c.twitter, c.sic_code_all, c.sic_text_all, c.sub_industry_1, c.industry_1, c.employees, c.employee_range, c.turnover, c.turnover_range, p.pid, p.title, p.first_name AS 'f_name', p.last_name AS 'l_name', p.job_title AS 'job_people', p.job_title_level, p.people_email, p.people_email_score, p.PersonLinkedin\nFROM infy_prod.infynd_uk_product_company c\nJOIN infy_prod.infynd_uk_product_people p ON c.akey = p.akey\nWHERE c.industry = 'Farming'\n  AND c.Country = 'England'\n  AND p.job_title_level IN ('Director', 'senior', 'C level', 'VP_level', 'Company Secretary')\n  AND c.exclude_flag = 0\n  AND p.exclude_flag = 0;\n```\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "give me educational related company with sic code 4200,4599 and are located in bedfordshire , bristol and bedford and have websites",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```sql\nSELECT \n    akey,\n    company_registration_number,\n    CompanyName,\n    Address_Line_1,\n    Address_Line_2,\n    Address_Line_3,\n    Post_Town,\n    County,\n    Post_Code,\n    phone AS 'db_phone',\n    website,\n    linkedin,\n    facebook,\n    twitter,\n    sic_code_all,\n    sic_text_all,\n    sub_industry_1,\n    industry_1,\n    employees,\n    employee_range,\n    turnover,\n    turnover_range\nFROM\n    infy_prod.infynd_uk_product_company\nWHERE \n    (sic_code1 IN ('4200','4599') OR sic_code2 IN ('4200','4599') OR sic_code3 IN ('4200','4599') OR sic_code4 IN ('4200','4599'))\n    AND Post_Town IN ('Bristol','Bedford') AND county ='Bedfordshire' AND website_1 = 1\n    AND sector = 'Education'\n    AND exclude_flag = 0;\n```\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "give me sdm level people working in it",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```sql\nSELECT pid, title, first_name AS 'f_name', last_name AS 'l_name', job_title AS 'job_people', job_title_level, people_email, people_email_score, PersonLinkedin FROM infy_prod.infynd_uk_product_people WHERE job_title_level IN ('Director','senior','C level','VP_level','Company Secretary') AND job_title LIKE '%IT%' AND exclude_flag=0\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "give me sdm level valid people",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```sql\nSELECT pid, title, first_name AS 'f_name', last_name AS 'l_name', job_title AS 'job_people', job_title_level, people_email, people_email_score, PersonLinkedin FROM infy_prod.infynd_uk_product_people WHERE job_title_level IN ('Director','senior','C level','VP_level','Company Secretary') AND people_email_score >= 83 AND exclude_flag=0\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "give me pubs , bars, restaurants, advertising, housebuilder developer,property developers,contruction,builders",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```sql\nSELECT \n    akey,\n    company_registration_number,\n    CompanyName,\n    Address_Line_1,\n    Address_Line_2,\n    Address_Line_3,\n    Post_Town,\n    County,\n    Post_Code,\n    phone AS 'db_phone',\n    website,\n    linkedin,\n    facebook,\n    twitter,\n    sic_code_all,\n    sic_text_all,\n    sub_industry_1,\n    industry_1,\n    employees,\n    employee_range,\n    turnover,\n    turnover_range\nFROM\n    infy_prod.infynd_uk_product_company\nWHERE \n    (\n        industry IN ('Food and Beverage Services', 'Advertising Services', 'Building Construction')\n        OR sub_industry IN ('Pubs, Bars & Inns', 'Bars', 'Restaurants', 'Property Developers', 'Builders/construction Firm', 'Home/house Builders', 'Construction Contractors/builders',\n                             'African Restaurants', 'American Restaurants', 'Argentinian Restaurants', 'Brazilian Restaurants', 'Caribbean Restaurants', 'Chinese Restaurants', 'English Restaurants', \n                             'French Restaurants', 'Greek Restaurants', 'Indian Restaurants', 'Italian Restaurants', 'Japanese Restaurants', 'Lebanese Restaurants', 'Mediterranean Restaurants', \n                             'Mexican Restaurants', 'Nepalese Restaurants', 'Oriental Restaurants', 'Portuguese Restaurants', 'Russian Restaurants', 'Scottish Restaurants', 'Seafood Restaurants', \n                             'Spanish Restaurants', 'Thai Restaurants', 'Turkish Restaurants', 'Vietnamese Restaurants'\n                            )\n        OR sector = 'Construction' \n    )\n    AND exclude_flag = 0;\n```\n",
      ],
    },
  ]
)

    # Input from user
    user_input = st.text_input("Enter your query:")

    if user_input:
        # Send the user's input to the model
        try:
            response = chat_session.send_message(user_input)
            st.write("Generated SQL Query:")
            st.code(response.text, language="sql")
        except Exception as e:
            st.error(f"Failed to get response from model: {e}")

if __name__ == "__main__":
    main()
