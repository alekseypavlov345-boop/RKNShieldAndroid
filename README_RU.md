# RKN Shield Android v2

Android-приложение для выборочного направления Telegram, WhatsApp, Instagram и YouTube через защищённый WireGuard-туннель.

## Что уже реализовано

- Одна основная кнопка **ОБХОД ВКЛ / ОБХОД ВЫКЛ**.
- Отдельные переключатели Telegram, WhatsApp, Instagram и YouTube.
- В VPN попадают только выбранные приложения, которые реально установлены на телефоне.
- Импорт обычного WireGuard `.conf` через системный выбор файла.
- Конфигурация хранится в приватном каталоге приложения.
- Для сборки GitHub Actions добавлен workflow, который выпускает debug APK как artifact.
- Root не требуется.

## Важное отличие от ByeDPI / Zapret

Эта v2 использует полноценный WireGuard-туннель. Поэтому ей нужен рабочий WireGuard endpoint и конфигурация `.conf`. Это сделано специально, чтобы трафик выбранных приложений можно было надёжно провести через другой сетевой маршрут целиком, а не только пытаться изменить отдельные DPI-признаки соединения.

Serverless-режим уровня ByeDPI, где внешний VPN-сервер не нужен, является отдельным сетевым backend и не включён в эту сборку.

## Как запустить

1. Открой проект в Android Studio с JDK 17.
2. Дождись Gradle Sync.
3. Собери `app` и установи APK на Android 6.0+.
4. В приложении нажми **Импортировать WireGuard .conf** и выбери рабочую конфигурацию.
5. Оставь включёнными нужные приложения.
6. Нажми **ОБХОД ВКЛ** и один раз подтверди системное разрешение VPN.

## Поддерживаемые package names

- Telegram: `org.telegram.messenger`, `org.telegram.messenger.web`, `org.thunderdog.challegram`
- WhatsApp: `com.whatsapp`, `com.whatsapp.w4b`
- Instagram: `com.instagram.android`
- YouTube: `com.google.android.youtube`

## Безопасность конфигурации

WireGuard `.conf` обычно содержит приватный ключ. RKN Shield сохраняет импортированный файл только во внутреннее хранилище приложения. Не публикуй свою реальную конфигурацию в GitHub и не добавляй её в исходники.

## Сборка в GitHub Actions

Workflow `.github/workflows/android.yml` собирает `app-debug.apk` и сохраняет его как artifact `RKNShield-v2-debug-apk`.
