# prompt-flow-prototyping
Prompt flow custom code 3 nodes

The key point here is that you can use a prompt flow from the folder to get idea how to start with prototyping and building of the new solution with Python and PromptFlow

The key component is the YAML flow, but you need a full sample to make it work.

```YAML
inputs:
  chat_input:
    type: string
    is_chat_input: true
  chat_history:
    type: string
    is_chat_input: false
outputs:
  chat_output:
    type: string
    reference: ${summary.output}
    is_chat_output: true
nodes:
- name: search_indexed_docs
  type: python
  source:
    type: package
    tool: promptflow_vectordb.tool.common_index_lookup.search
  inputs:
    mlindex_content: >
      embeddings:
        api_base: https://stas.openai.azure.com/
        api_type: azure
        api_version: 2023-07-01-preview
        batch_size: '16'
        connection:
          id: /subscriptions/1df8c/resourceGroups/ml-experiments/providers/Microsoft.MachineLearningServices/workspaces/stas/connections/gpt4
        connection_type: workspace_connection
        deployment: embedding
        dimension: 1536
        file_format_version: '2'
        kind: open_ai
        model: text-embedding-ada-002
        schema_version: '2'
      index:
        api_version: 2023-07-01-preview
        connection:
          id: /subscriptions/1df8c/resourceGroups/ml-experiments/providers/Microsoft.MachineLearningServices/workspaces/stas/connections/Search
        connection_type: workspace_connection
        endpoint: https://stas.search.windows.net
        engine: azure-sdk
        field_mapping:
          content: content
          embedding: contentVector
          filename: filepath
          metadata: meta_json_string
          title: title
          url: url
        index: quiet-spider-gy4cgsryhh
        kind: acs
        semantic_configuration_name: azureml-default
    queries: ${inputs.chat_input}
    query_type: Vector
    top_k: 2
  use_variants: false
- name: generate_prompt_context
  type: python
  source:
    type: code
    path: generate_prompt_context.py
  inputs:
    search_result: ${search_indexed_docs.output}
  use_variants: false
- name: Prompt_variants
  type: prompt
  source:
    type: code
    path: Prompt_variants.jinja2
  inputs:
    chat_history: ${inputs.chat_history}
    contexts: ${generate_prompt_context.output}
    question: ${inputs.chat_input}
  use_variants: false
- name: prompt_variants_no_data
  use_variants: true
- name: Chat_without_data
  type: llm
  source:
    type: code
    path: Chat_with_context_2.jinja2
  inputs:
    deployment_name: Turbo-4
    temperature: 0.5
    top_p: 1
    max_tokens: 3000
    presence_penalty: 0
    frequency_penalty: 0
    prompt_text: ${prompt_variants_no_data.output}
  provider: AzureOpenAI
  connection: gpt4
  api: chat
  module: promptflow.tools.aoai
  use_variants: false
- name: Chat_with_context
  type: llm
  source:
    type: code
    path: chat_with_context.jinja2
  inputs:
    deployment_name: Turbo-4
    temperature: 0.5
    top_p: 1
    max_tokens: 3000
    presence_penalty: 0
    frequency_penalty: 0
    prompt_text: ${Prompt_variants.output}
  provider: AzureOpenAI
  connection: gpt4
  api: chat
  module: promptflow.tools.aoai
  use_variants: false
- name: summary
  type: llm
  source:
    type: code
    path: summary.jinja2
  inputs:
    deployment_name: Turbo-4
    temperature: 0.5
    top_p: 1
    max_tokens: 3000
    presence_penalty: 0
    frequency_penalty: 0
    answer1: ${Chat_without_data.output}
    answer2: ${Chat_with_context.output}
    answer3: ${Custom_code.output}
  provider: AzureOpenAI
  connection: gpt4
  api: chat
  module: promptflow.tools.aoai
  use_variants: false
- name: Custom_code
  type: python
  source:
    type: code
    path: Classificator.py
  inputs:
    input1: ${pip_install.output}
  use_variants: false
- name: pip_install
  type: python
  source:
    type: code
    path: pip_install.py
  inputs:
    input1: ${inputs.chat_input}
  use_variants: false
node_variants:
  prompt_variants_no_data:
    default_variant_id: variant_0
    variants:
      variant_0:
        node:
          name: prompt_variants_no_data
          type: prompt
          source:
            type: code
            path: direct_variants.jinja2
          inputs:
            chat_input: ${inputs.chat_input}
      variant_1:
        node:
          name: prompt_variants_no_data
          type: prompt
          source:
            type: code
            path: prompt_variants_no_data__variant_1.jinja2
          inputs:
            chat_input: ${inputs.chat_input}
      variant_2:
        node:
          name: prompt_variants_no_data
          type: prompt
          source:
            type: code
            path: prompt_variants_no_data__variant_2.jinja2
          inputs:
            chat_input: ${inputs.chat_input}
      variant_3:
        node:
          name: prompt_variants_no_data
          type: prompt
          source:
            type: code
            path: prompt_variants_no_data__variant_3.jinja2
          inputs:
            chat_input: ${inputs.chat_input}
      variant_4:
        node:
          name: prompt_variants_no_data
          type: prompt
          source:
            type: code
            path: prompt_variants_no_data__variant_4.jinja2
          inputs:
            chat_input: ${inputs.chat_input}
      variant_5:
        node:
          name: prompt_variants_no_data
          type: prompt
          source:
            type: code
            path: prompt_variants_no_data__variant_5.jinja2
          inputs:
            chat_input: ${inputs.chat_input}
environment:
  python_requirements_txt: requirements.txt
```
