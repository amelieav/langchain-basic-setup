# Langchain basic setup

basic_setup.py demonstrates how to:
- Load environment variables from a .env file for secure access to API keys
- Use OpenAI's API using ChatOpenAI from LangChain
- Construct structured AI prompts using ChatPromptTemplate
- Parse AI model outputs with StrOutputParser
- Retrieve and load web documents for data processing using WebBaseLoader
- Create text embeddings for document processing with OpenAIEmbeddings
- Implement in-memory document search using DocArrayInMemorySearch
- Prepare documents for processing with RecursiveCharacterTextSplitter
- Log input queries and AI responses for record-keeping.

moderation_setup.py demonstrates how to:
- Configure and use the OpenAI API for content moderation
- Define a function to send text to the OpenAI moderation API and interpret the response
- Evaluate text to determine if it violates OpenAI's content policies using the moderation API
- Parse and display detailed moderation results, including flagged status and category scores
- Handle network and API request errors gracefully
- Test moderation function with sample text input










