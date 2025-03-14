
def model_name(model_type):
  
    if model_type == 'GPT-4o':
        model='gpt-4o'
    elif model_type == 'DeepSeek':
        model='deepseek/deepseek-chat'
    elif model_type == 'Claude':
        model='claude-3-7-sonnet-20250219'
    elif model_type == 'Grok':
        model='xai/grok-2-latest'
    else:
        model='gemini/gemini-2.0-flash-exp'

    return model


def pricing(selected_model, input_tokens, output_tokens):

    if selected_model == 'GPT-4o':
        input_tokens_total = input_tokens * (2.50 / 1000000)
        output_tokens_total = output_tokens * (10 / 1000000)


    elif selected_model == 'DeepSeek':
        input_tokens_total = input_tokens * (0.27 / 1000000)
        output_tokens_total = output_tokens * (1.10 / 1000000)


    elif selected_model == 'Claude':
        input_tokens_total = input_tokens * (3 / 1000000)
        output_tokens_total = output_tokens * (15 / 1000000)


    elif selected_model == 'Grok':
        input_tokens_total = input_tokens * (2 / 1000000)
        output_tokens_total = output_tokens * (10 / 1000000)


    else:
        input_tokens_total = input_tokens * (0.1 / 1000000)
        output_tokens_total = output_tokens * (0.4 / 1000000)

    total = input_tokens_total + output_tokens_total

    return round(total, 4)  
