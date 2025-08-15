## .vscode/settings.json
{
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "github.copilot.chat.commitMessageGeneration.instructions": [
        {
            "file": ".github/instructions/gitmoji.instructions.md"
        }
    ],
    "github.copilot.chat.reviewSelection.instructions": [
        {
            "text": "When reviewing code, Respond in Korean."
        }
    ]
}

## .github/instructions/conventional_commits_ko.instructions.md
# Commit Message Format

When making changes to the codebase, please follow the conventional commits format.
This helps maintain a clear and consistent commit history.

The format is as follows:

```
<type>[optional scope]: <subject>

[optional body]

[optional footer(s)]
```

* **type**: 변경의 종류를 나타내는 한 단어(`feat`, `fix`, `docs`, `refactor`, `test`, `chore` …).
* **scope**: 영향 범위(모듈·폴더 등)를 괄호로 표기하며 생략 가능.
* **subject**: 50자 이내, 명령형 현재 시제, 첫 글자 소문자, 마침표 금지.
* 한글 커밋도 허용하지만 `type`, `scope` 는 영문으로 유지합니다.

## type

* **feat** — 새로운 기능 (SemVer *minor*)
* **fix** — 버그 수정 (SemVer *patch*)
* **docs** — 문서만의 변경
* **style** — 포맷·세미콜론 등 논리적 변경 없는 코드 스타일 수정
* **refactor** — 리팩터링(기능 추가·버그 수정 아님)
* **perf** — 성능 개선
* **test** — 테스트 추가·수정
* **build** — 빌드 시스템·외부 의존성 변경
* **ci** — CI 설정·스크립트 변경
* **chore** — 잡무(빌드 설정, 의존성 업데이트 등)
* **revert** — 이전 커밋 되돌리기


## .github/instructions/conventional_commits_en.instructions.md
# Commit Message Format

When making changes to the codebase, please follow the **Conventional Commits** format. This helps maintain a clear and consistent commit history.

The format is as follows:

```
<type>[optional scope]: <subject>

[optional body]

[optional footer(s)]
```

* **type**: A single word that describes the kind of change (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`, …).
* **scope**: The affected area (module, folder, etc.) in parentheses; optional.
* **subject**: Imperative, present tense, up to 50 characters; start with a lowercase letter; no period at the end.

## type

* **feat** — a new feature (SemVer *minor*)
* **fix** — a bug fix (SemVer *patch*)
* **docs** — documentation‑only changes
* **style** — formatting, semicolons, etc.; no logical code changes
* **refactor** — refactoring (neither adding features nor fixing bugs)
* **perf** — performance improvements
* **test** — adding or modifying tests
* **build** — changes to the build system or external dependencies
* **ci** — changes to CI configuration or scripts
* **chore** — maintenance tasks (build settings, dependency updates, etc.)
* **revert** — revert a previous commit

## Tips for Writing Good Commit Messages

1. Focus on **“what” and “why”**; let the code explain **“how.”**
2. Wrap the body at 72 characters to improve compatibility with terminals and tools.
3. Even when writing the body in Korean, separate the header and body with a blank line.
4. Commit early and often, even for small changes, to keep the history granular.



## .github/instructions/gitmoji.instructions.md
# Gitmoji Commit Message Format

커밋 메시지에 **Gitmoji**를 더해, 변경의 성격을 한눈에 알 수 있도록 하세요. Conventional Commits 규칙과 함께 사용하면 기록이 명확하고 즐거워집니다.

---

## Format

```
<emoji> <type>[optional scope]: <subject>

[optional body]

[optional footer(s)]
```

* **emoji**: 변경 종류를 나타내는 Gitmoji 하나.
* **type**: `feat`, `fix`, `docs` … 와 같은 Conventional Commit 타입.
* **scope**: 영향 범위(모듈·폴더 등)를 괄호로 표기하며 생략 가능.
* **subject**: 50자 이내, 명령형 현재 시제, 첫 글자 소문자, 마침표 금지.
* 한글 커밋도 허용하지만 `emoji`, `type`, `scope` 는 그대로 유지합니다.

---

## Emoji ↔︎ Type 매핑

* ✨ **feat** — 새로운 기능 (SemVer *minor*)
* 🐛 **fix** — 버그 수정 (SemVer *patch*)
* 📝 **docs** — 문서만의 변경
* 🎨 **style** — 포맷·세미콜론 등 논리적 변경 없는 코드 스타일 수정
* ♻️ **refactor** — 리팩터링 (기능 추가·버그 수정 아님)
* ⚡️ **perf** — 성능 개선
* ✅ **test** — 테스트 추가·수정
* 🏗 **build** — 빌드 시스템·외부 의존성 변경
* 👷 **ci** — CI 설정·스크립트 변경
* 🔧 **chore** — 잡무(빌드 설정, 의존성 업데이트 등)
* ⏪ **revert** — 이전 커밋 되돌리기





## .github\instructions\custom_commits_ko.instructions.md
# Commit Message Format

When making changes to the codebase, please follow the conventional commits format.
This helps maintain a clear and consistent commit history.
Language: Korean for Text outputs

The format is as follows:


```
<type>[optional scope][optional ticket]: <subject>

[optional body]

[optional footer(s)]
```

* **type**: 변경의 종류를 나타내는 한 단어(`feat`, `fix`, `docs`, `refactor`, `test`, `chore` …).
* **scope**: 영향 범위(모듈·폴더 등)를 괄호로 표기하며 생략 가능.
* **ticket**: 이슈/티켓 번호를 대괄호로 표기하며 생략 가능. 예: `[LEC-001]`
* **subject**: 50자 이내, 명령형 현재 시제, 첫 글자 소문자, 마침표 금지.
* 한글 커밋도 허용하지만 `type`, `scope` 는 영문으로 유지합니다.

예시:
```
feat[LEC-001]:  코드 변경했음
fix(api)[LEC-002]: 버그 수정
docs: 문서만 변경
```

## type

* **feat** — 새로운 기능 (SemVer *minor*)
* **fix** — 버그 수정 (SemVer *patch*)
* **docs** — 문서만의 변경
* **style** — 포맷·세미콜론 등 논리적 변경 없는 코드 스타일 수정
* **refactor** — 리팩터링(기능 추가·버그 수정 아님)
* **perf** — 성능 개선
* **test** — 테스트 추가·수정
* **build** — 빌드 시스템·외부 의존성 변경
* **ci** — CI 설정·스크립트 변경
* **chore** — 잡무(빌드 설정, 의존성 업데이트 등)
* **revert** — 이전 커밋 되돌리기