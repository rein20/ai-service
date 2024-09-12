import requests

import gradio as gr


MAPPING_EN2KO = {
    "hangover": "해장",
    "diet": "다이어트"
}
MAPPING_KO2EN = {v: k for k, v in MAPPING_EN2KO.items()}


def get_recommendations(query_ko):
    query_en = MAPPING_KO2EN[query_ko]
    print(query_en)
    url = f"http://127.0.0.1:8000/recommend/{query_en}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()[0]
        print(data)
    else:
        print(f"Request failed with status code: {response.status_code}")

    return data


def fn(query_ko):
    recs = get_recommendations(query_ko)
    rec_reason = recs['recommend_reason'] + '\n\n'
    rec_items = ''
    for i, rec in enumerate(recs['recommendations']):
        rec_items += f'음식점 #{i+1}: ' + rec['restaurant'] + '\n'
        rec_items += '메뉴 목록:\n'
        for j, menu in enumerate(rec['menus']):
            rec_items += f'        #{j+1}: ' + menu + '\n'
        rec_items += '\n'
    return rec_reason, rec_items


def run_demo():
    demo = gr.Interface(
        title='먹어본 이웃의 한 마디 ♾',
        fn=fn,
        inputs=[gr.Radio(['해장', '다이어트'], label='GPT-4 활용 추천 ⓘ')],
        outputs=[gr.Textbox(label='추천 사유'), gr.Textbox(label='추천 아이템')]
    )
    demo.launch(share=True)


if __name__ == '__main__':
    run_demo()