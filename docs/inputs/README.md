# Input URLs

`urls.txt`에는 수집할 문서 URL을 한 줄에 하나씩 넣습니다.

예시:

```txt
https://developers.openai.com/api/docs/guides/reasoning
https://developers.openai.com/api/docs/guides/migrate-to-responses
```

생성 스크립트는 이 URL들을 읽어 문서 본문을 `docs/inputs/md/*.md`로 저장하고, 번역된 `docs/golden/*.json` 파일도 함께 다시 만듭니다.
