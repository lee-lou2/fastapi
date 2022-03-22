from conf.celery import app


@app.task
def ka_ka_o_ai(content):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM

    tokenizer = AutoTokenizer.from_pretrained(
        'kakaobrain/kogpt', revision='KoGPT6B-ryan1.5b',
        bos_token='[BOS]', eos_token='[EOS]', unk_token='[UNK]', pad_token='[PAD]', mask_token='[MASK]'
    )
    model = AutoModelForCausalLM.from_pretrained(
        'kakaobrain/kogpt', revision='KoGPT6B-ryan1.5b',
        pad_token_id=tokenizer.eos_token_id,
        torch_dtype=torch.float16, low_cpu_mem_usage=True
    ).to(device='cpu', non_blocking=True)
    _ = model.eval()

    prompt = f'''
    Q:{content}
    A:'''

    with torch.no_grad():
        tokens = tokenizer.encode(prompt, return_tensors='pt').to(device='cpu', non_blocking=True)
        gen_tokens = model.generate(tokens, do_sample=True, temperature=0.8, max_length=256)
        generated = tokenizer.batch_decode(gen_tokens)[0]

    # 슬랙 전송
    from apps.backend.service.notice.controllers.send import send_slack_background_task
    from apps.backend.service.notice.schemas import SendSlackRequest
    send_slack_background_task(SendSlackRequest(
        room='token',
        message=(
            '[ 카카오 AI ]\n\n'
            f'- 답변 : {generated}\n'
        )
    ))
    return None
