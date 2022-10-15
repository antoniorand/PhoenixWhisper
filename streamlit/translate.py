# installs
# !pip install --upgrade pytube git+https://github.com/openai/whisper.git -q
# !pip install sentencepiece -q
# !pip install transformers==4.13.0 -q
# !pip install --upgrade openai -q

# libraries
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import openai, json

translator = 'mtm' #'gpt'
openai.api_key = 'YOUR_OPENAI_APIKEY'

src_lang = ['en', 'english'] # source language
tgt_lang = ['de', 'german'] # target language

f = open("data.json")
output = json.load(f)

#### get translation ####
transcript_translated = []

# facebook multi lingual translation model
if translator == 'mtm':
  # get the model and tokenizer
  translator_model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
  tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

  # translate 
  tokenizer.src_lang = src_lang[0]

  # loop through transcription and translate
  for k, item in enumerate(output['segments']):
    src_text = item['text']

    encoded_text = tokenizer(src_text, return_tensors="pt")
    generated_tokens = translator_model.generate(**encoded_text, forced_bos_token_id=tokenizer.get_lang_id(tgt_lang[0]))
    tgt_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

    transcript_translated.append({'src_lang': src_lang[0], 'src': src_text, 'target_lang': tgt_lang[0], 'target': tgt_text[0]})
    
    # if k == 10:
    #   break

# gpt translation model
elif translator == 'gpt':
  # prompt
  prompt_base = 'Translate '+src_lang[1]+' to '+ tgt_lang[1]+ ': \n\n Todays is a beautiful day => Heute ist ein schöner Tag \n\n '

  # loop through transcription and translate
  for k, item in enumerate(output['segments']):
    src_text = item['text']

    # append text to prompt
    prompt = prompt_base + src_text + " => "

    # Note: rule of thumb to avoid random continuation
    max_tokens = 6*len(src_text.split())

    response = openai.Completion.create(
      model="text-curie-001", # text-davinci-002 -> bigger model for later
      prompt=prompt,
      temperature=0.1,
      max_tokens=max_tokens,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )

    # append to output
    transcript_translated.append({'src_lang': src_lang[0], 'src': src_text, 'target_lang': tgt_lang[0], 'target': response['choices'][0]['text']})

    if k == 10:
      break

# 
else:
  print('Plese choose a tranlsation model {mtm, gpt}')

# print output to check
print(transcript_translated)