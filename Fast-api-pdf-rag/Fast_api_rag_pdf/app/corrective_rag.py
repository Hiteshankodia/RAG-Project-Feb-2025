from app.conversation_chain import get_conversational_chain


def correct_response_with_documents(initial_answer: str, docs: list, query : str) -> str:
    """
    Function to apply corrective RAG to improve or refine the initial answer using the retrieved documents.
    This could involve re-running a generation chain or adjusting the result based on retrieved context.
    """
    # You can either rerun the generation model with refined context, or manually adjust the output.
    # Example: re-run the model with more context or documents.

    # Option 1: Concatenate additional context to the original answer
    print('Type: ---',type(docs))
    
    refined_query = f"Question: {query} \nAnswer: {initial_answer} \nHere are some additional documents:\n" + "\n".join([doc.page_content for doc in docs])

    # Re-run the conversational chain with the refined context
    corrected_response = get_conversational_chain()(
        {"input_documents": docs, "question": refined_query},
        return_only_outputs=True
    )

    return corrected_response["output_text"]