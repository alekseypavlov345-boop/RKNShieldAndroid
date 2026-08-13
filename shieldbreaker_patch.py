from pathlib import Path
import re

ROOT = Path("upstream")
APP = ROOT / "app"

# Identity/version.
gradle = APP / "build.gradle.kts"
text = gradle.read_text(encoding="utf-8")
text = text.replace('applicationId = "io.github.romanvht.byedpi"', 'applicationId = "com.shieldbreaker.android"')
text = text.replace('versionCode = 1770', 'versionCode = 4000')
text = text.replace('versionName = "1.7.7"', 'versionName = "1.0"')
gradle.write_text(text, encoding="utf-8")

# Brand strings.
for strings in (APP / "src/main/res").glob("values*/strings.xml"):
    text = strings.read_text(encoding="utf-8")
    text = text.replace("ByeByeDPI", "ShieldBreaker")
    strings.write_text(text, encoding="utf-8")

ru_strings = APP / "src/main/res/values/strings.xml"
text = ru_strings.read_text(encoding="utf-8")
replacements = {
    '<string name="vpn_connected">Подключено (VPN)</string>': '<string name="vpn_connected">Защита включена</string>',
    '<string name="vpn_disconnected">Отключено (VPN)</string>': '<string name="vpn_disconnected">Защита выключена</string>',
    '<string name="vpn_notification_content">VPN работает</string>': '<string name="vpn_notification_content">Локальная защита активна</string>',
    '<string name="title_test">Подбор стратегий</string>': '<string name="title_test">Автоподбор соединения</string>',
    '<string name="summary_test">Тестирование работы подготовленных аргументов командной строки</string>': '<string name="summary_test">Проверка встроенных локальных стратегий</string>',
}
for old, new in replacements.items():
    text = text.replace(old, new)
ru_strings.write_text(text, encoding="utf-8")

# Balanced local DPI profile.
prefs = APP / "src/main/java/io/github/romanvht/byedpi/utility/PreferencesUtils.kt"
text = prefs.read_text(encoding="utf-8")
old = 'private const val DEFAULT_CMD_ARGS = "-o1 -a1 -r-5+se"'
new = 'private const val DEFAULT_CMD_ARGS = "-Ku -a5 -t4 -An -Kh -Mh,d -An -Kt -d3 -s25+s -An"'
if old not in text:
    raise SystemExit("DEFAULT_CMD_ARGS marker not found")
text = text.replace(old, new)

old_apps = '''fun SharedPreferences.getSelectedApps(): List<String> {
    return getStringSet("selected_apps", emptySet())?.toList() ?: emptyList()
}'''
new_apps = '''fun SharedPreferences.getSelectedApps(): List<String> {
    val defaults = setOf(
        "com.google.android.youtube",
        "org.telegram.messenger",
        "org.telegram.messenger.web",
        "org.thunderdog.challegram",
        "com.whatsapp",
        "com.whatsapp.w4b",
        "com.instagram.android"
    )
    return getStringSet("selected_apps", defaults)?.toList() ?: defaults.toList()
}'''
if old_apps not in text:
    raise SystemExit("getSelectedApps marker not found")
prefs.write_text(text.replace(old_apps, new_apps), encoding="utf-8")

# Default app filter = whitelist.
main_settings = APP / "src/main/res/xml/main_settings.xml"
text = main_settings.read_text(encoding="utf-8")
text = text.replace('android:defaultValue="disable" />', 'android:defaultValue="whitelist" />', 1)
main_settings.write_text(text, encoding="utf-8")

vpn = APP / "src/main/java/io/github/romanvht/byedpi/services/ByeDpiVpnService.kt"
text = vpn.read_text(encoding="utf-8")
text = text.replace('builder.setSession("ByeDPI")', 'builder.setSession("ShieldBreaker")')
text = text.replace('getStringNotNull("applist_type", "disable")', 'getStringNotNull("applist_type", "whitelist")')
vpn.write_text(text, encoding="utf-8")

# Original ShieldBreaker vector logo.
drawable = APP / "src/main/res/drawable"
(drawable / "shieldbreaker_logo.xml").write_text('''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path android:fillColor="#07111F" android:pathData="M54,3 A51,51 0,1 1,53.9 3Z"/>
    <path android:fillColor="#0B1D33" android:strokeColor="#203B60" android:strokeWidth="3"
        android:pathData="M54,8 A46,46 0,1 1,53.9 8Z"/>
    <path android:fillColor="#26384D" android:strokeColor="#DCE8F5" android:strokeWidth="3.4"
        android:strokeLineJoin="round"
        android:pathData="M54,21 L82,31 L78,63 C76,76 68,87 54,95 C40,87 32,76 30,63 L26,31 Z"/>
    <path android:fillColor="#111C2B"
        android:pathData="M54,27 L75,34 L72,62 C70,72 64,81 54,87 C44,81 38,72 36,62 L33,34 Z"/>
    <path android:fillColor="#38BDF8" android:fillAlpha="0.55"
        android:pathData="M50,49 L56,55 L49,61 L43,55 Z"/>
    <path android:strokeColor="#60A5FA" android:strokeWidth="2" android:strokeLineCap="round"
        android:pathData="M52,53 L42,41 M52,55 L40,66 M56,55 L67,44 M56,58 L69,69"/>
    <path android:fillColor="#DDE9F6" android:strokeColor="#FFFFFF" android:strokeWidth="1.4"
        android:pathData="M70,16 L78,20 L45,91 L35,87 Z"/>
    <path android:fillColor="#22D3EE"
        android:pathData="M71.5,20 L75.2,21.7 L43.2,88 L39.5,86.4 Z"/>
    <path android:fillColor="#EAF5FF"
        android:pathData="M65,25 L84,34 L81,39 L62,30 Z"/>
    <path android:fillColor="#1B2A40" android:strokeColor="#BFD7EE" android:strokeWidth="1.2"
        android:pathData="M74,8 L82,12 L77,25 L69,21 Z"/>
    <path android:fillColor="#3B82F6" android:strokeColor="#DFF7FF" android:strokeWidth="1.2"
        android:pathData="M77,6 A6,6 0,1 1,76.9 6Z"/>
</vector>''', encoding="utf-8")

# Launcher icon.
manifest = APP / "src/main/AndroidManifest.xml"
text = manifest.read_text(encoding="utf-8")
text = re.sub(r'android:icon="@mipmap/[^"]+"', 'android:icon="@drawable/shieldbreaker_logo"', text)
text = re.sub(r'android:roundIcon="@mipmap/[^"]+"', 'android:roundIcon="@drawable/shieldbreaker_logo"', text)
manifest.write_text(text, encoding="utf-8")

# Quick badge drawables.
badge_colors = {
    "shieldbreaker_app_badge_red.xml": "#E53935",
    "shieldbreaker_app_badge_blue.xml": "#229ED9",
    "shieldbreaker_app_badge_green.xml": "#22C55E",
    "shieldbreaker_app_badge_purple.xml": "#A855F7",
    "shieldbreaker_info_badge.xml": "#0A2138",
}
for name, color in badge_colors.items():
    (drawable / name).write_text(f'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="oval">
    <solid android:color="{color}" />
</shape>''', encoding="utf-8")

# New home screen.
layout = APP / "src/main/res/layout/activity_main.xml"
layout.write_text('''<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:fillViewport="true"
    android:background="#060A10"
    android:overScrollMode="never">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:paddingStart="20dp"
        android:paddingEnd="20dp"
        android:paddingTop="24dp"
        android:paddingBottom="24dp">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:gravity="center_vertical"
            android:orientation="horizontal">
            <Space android:layout_width="48dp" android:layout_height="48dp" />
            <LinearLayout
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:gravity="center"
                android:orientation="vertical">
                <ImageView
                    android:layout_width="132dp"
                    android:layout_height="132dp"
                    android:contentDescription="ShieldBreaker"
                    android:src="@drawable/shieldbreaker_logo" />
                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:layout_marginTop="8dp"
                    android:text="ShieldBreaker"
                    android:textColor="#F5F8FC"
                    android:textSize="30sp"
                    android:textStyle="bold" />
                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:layout_marginTop="2dp"
                    android:text="LOCAL DPI BYPASS"
                    android:textColor="#3BA5FF"
                    android:textSize="11sp"
                    android:letterSpacing="0.18" />
            </LinearLayout>
            <com.google.android.material.card.MaterialCardView
                android:id="@+id/settings_button"
                android:layout_width="48dp"
                android:layout_height="48dp"
                android:clickable="true"
                android:focusable="true"
                android:foreground="?attr/selectableItemBackground"
                app:cardBackgroundColor="#0C1420"
                app:cardCornerRadius="24dp"
                app:strokeColor="#1E344E"
                app:strokeWidth="1dp">
                <ImageView
                    android:layout_width="24dp"
                    android:layout_height="24dp"
                    android:layout_gravity="center"
                    android:src="@drawable/baseline_settings_24"
                    app:tint="#A9BDD2" />
            </com.google.android.material.card.MaterialCardView>
        </LinearLayout>

        <com.google.android.material.card.MaterialCardView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_gravity="center_horizontal"
            android:layout_marginTop="14dp"
            app:cardBackgroundColor="#091827"
            app:cardCornerRadius="22dp"
            app:strokeColor="#1768B5"
            app:strokeWidth="1dp">
            <TextView
                android:id="@+id/status_text"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:paddingStart="20dp"
                android:paddingEnd="20dp"
                android:paddingTop="10dp"
                android:paddingBottom="10dp"
                android:text="Защита выключена"
                android:textColor="#3BA5FF"
                android:textSize="15sp"
                android:textStyle="bold" />
        </com.google.android.material.card.MaterialCardView>

        <com.google.android.material.card.MaterialCardView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="22dp"
            app:cardBackgroundColor="#09111B"
            app:cardCornerRadius="22dp"
            app:strokeColor="#17283B"
            app:strokeWidth="1dp">
            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:gravity="center"
                android:orientation="vertical"
                android:paddingTop="24dp"
                android:paddingBottom="22dp">
                <com.google.android.material.card.MaterialCardView
                    android:id="@+id/status_button_card"
                    android:layout_width="150dp"
                    android:layout_height="150dp"
                    android:clickable="true"
                    android:focusable="true"
                    android:foreground="?attr/selectableItemBackground"
                    app:cardBackgroundColor="#0B1B2E"
                    app:cardCornerRadius="75dp"
                    app:cardElevation="10dp"
                    app:strokeColor="#1E90FF"
                    app:strokeWidth="5dp">
                    <ImageView
                        android:id="@+id/status_button_icon"
                        android:layout_width="58dp"
                        android:layout_height="58dp"
                        android:layout_gravity="center"
                        android:contentDescription="ВКЛ / ВЫКЛ"
                        android:src="@drawable/ic_power"
                        app:tint="#F5FAFF" />
                </com.google.android.material.card.MaterialCardView>
                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:layout_marginTop="14dp"
                    android:text="ВКЛ / ВЫКЛ"
                    android:textColor="#F7FAFD"
                    android:textSize="22sp"
                    android:textStyle="bold" />
                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:layout_marginTop="4dp"
                    android:text="Нажмите для переключения"
                    android:textColor="#8193A8"
                    android:textSize="13sp" />
            </LinearLayout>
        </com.google.android.material.card.MaterialCardView>

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginTop="22dp"
            android:layout_marginBottom="10dp"
            android:text="Быстрые приложения"
            android:textColor="#F4F7FB"
            android:textSize="18sp"
            android:textStyle="bold" />

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:weightSum="4">

            <com.google.android.material.card.MaterialCardView
                android:layout_width="0dp"
                android:layout_height="132dp"
                android:layout_weight="1"
                android:layout_marginEnd="4dp"
                app:cardBackgroundColor="#0B131E"
                app:cardCornerRadius="16dp"
                app:strokeColor="#1A2A3D"
                app:strokeWidth="1dp">
                <LinearLayout android:layout_width="match_parent" android:layout_height="match_parent"
                    android:gravity="center" android:orientation="vertical" android:padding="8dp">
                    <TextView android:layout_width="42dp" android:layout_height="42dp"
                        android:background="@drawable/shieldbreaker_app_badge_red" android:gravity="center"
                        android:text="YT" android:textColor="#FFFFFF" android:textSize="14sp" android:textStyle="bold" />
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content"
                        android:layout_marginTop="7dp" android:text="YouTube" android:textColor="#F0F4F8"
                        android:textSize="12sp" android:textStyle="bold" />
                    <com.google.android.material.switchmaterial.SwitchMaterial
                        android:id="@+id/switch_youtube" android:layout_width="wrap_content"
                        android:layout_height="wrap_content" android:layout_marginTop="2dp" android:checked="true" />
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>

            <com.google.android.material.card.MaterialCardView
                android:layout_width="0dp" android:layout_height="132dp" android:layout_weight="1"
                android:layout_marginStart="4dp" android:layout_marginEnd="4dp"
                app:cardBackgroundColor="#0B131E" app:cardCornerRadius="16dp"
                app:strokeColor="#1A2A3D" app:strokeWidth="1dp">
                <LinearLayout android:layout_width="match_parent" android:layout_height="match_parent"
                    android:gravity="center" android:orientation="vertical" android:padding="8dp">
                    <TextView android:layout_width="42dp" android:layout_height="42dp"
                        android:background="@drawable/shieldbreaker_app_badge_blue" android:gravity="center"
                        android:text="TG" android:textColor="#FFFFFF" android:textSize="14sp" android:textStyle="bold" />
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content"
                        android:layout_marginTop="7dp" android:text="Telegram" android:textColor="#F0F4F8"
                        android:textSize="12sp" android:textStyle="bold" />
                    <com.google.android.material.switchmaterial.SwitchMaterial
                        android:id="@+id/switch_telegram" android:layout_width="wrap_content"
                        android:layout_height="wrap_content" android:layout_marginTop="2dp" android:checked="true" />
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>

            <com.google.android.material.card.MaterialCardView
                android:layout_width="0dp" android:layout_height="132dp" android:layout_weight="1"
                android:layout_marginStart="4dp" android:layout_marginEnd="4dp"
                app:cardBackgroundColor="#0B131E" app:cardCornerRadius="16dp"
                app:strokeColor="#1A2A3D" app:strokeWidth="1dp">
                <LinearLayout android:layout_width="match_parent" android:layout_height="match_parent"
                    android:gravity="center" android:orientation="vertical" android:padding="8dp">
                    <TextView android:layout_width="42dp" android:layout_height="42dp"
                        android:background="@drawable/shieldbreaker_app_badge_green" android:gravity="center"
                        android:text="WA" android:textColor="#FFFFFF" android:textSize="14sp" android:textStyle="bold" />
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content"
                        android:layout_marginTop="7dp" android:text="WhatsApp" android:textColor="#F0F4F8"
                        android:textSize="12sp" android:textStyle="bold" />
                    <com.google.android.material.switchmaterial.SwitchMaterial
                        android:id="@+id/switch_whatsapp" android:layout_width="wrap_content"
                        android:layout_height="wrap_content" android:layout_marginTop="2dp" android:checked="true" />
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>

            <com.google.android.material.card.MaterialCardView
                android:layout_width="0dp" android:layout_height="132dp" android:layout_weight="1"
                android:layout_marginStart="4dp"
                app:cardBackgroundColor="#0B131E" app:cardCornerRadius="16dp"
                app:strokeColor="#1A2A3D" app:strokeWidth="1dp">
                <LinearLayout android:layout_width="match_parent" android:layout_height="match_parent"
                    android:gravity="center" android:orientation="vertical" android:padding="8dp">
                    <TextView android:layout_width="42dp" android:layout_height="42dp"
                        android:background="@drawable/shieldbreaker_app_badge_purple" android:gravity="center"
                        android:text="IG" android:textColor="#FFFFFF" android:textSize="14sp" android:textStyle="bold" />
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content"
                        android:layout_marginTop="7dp" android:text="Instagram" android:textColor="#F0F4F8"
                        android:textSize="12sp" android:textStyle="bold" />
                    <com.google.android.material.switchmaterial.SwitchMaterial
                        android:id="@+id/switch_instagram" android:layout_width="wrap_content"
                        android:layout_height="wrap_content" android:layout_marginTop="2dp" android:checked="true" />
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>
        </LinearLayout>

        <com.google.android.material.card.MaterialCardView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="20dp"
            app:cardBackgroundColor="#0A131D"
            app:cardCornerRadius="18dp"
            app:strokeColor="#15273A"
            app:strokeWidth="1dp">
            <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content"
                android:gravity="center_vertical" android:orientation="horizontal" android:padding="16dp">
                <TextView android:layout_width="48dp" android:layout_height="48dp"
                    android:background="@drawable/shieldbreaker_info_badge" android:gravity="center"
                    android:text="✓" android:textColor="#3BA5FF" android:textSize="22sp" android:textStyle="bold" />
                <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content"
                    android:layout_marginStart="14dp" android:layout_weight="1" android:orientation="vertical">
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content"
                        android:text="Работает локально" android:textColor="#F0F4F8" android:textSize="15sp"
                        android:textStyle="bold" />
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content"
                        android:layout_marginTop="3dp"
                        android:text="Без VPS, серверов и .conf. Настройки хранятся только на устройстве."
                        android:textColor="#8FA2B8" android:textSize="12sp" />
                </LinearLayout>
            </LinearLayout>
        </com.google.android.material.card.MaterialCardView>

        <TextView android:id="@+id/proxy_address" android:layout_width="1dp" android:layout_height="1dp" android:visibility="gone" />
        <com.google.android.material.card.MaterialCardView android:id="@+id/editor_button"
            android:layout_width="1dp" android:layout_height="1dp" android:visibility="gone" />
        <LinearLayout android:id="@+id/cmd_buttons_row" android:layout_width="1dp" android:layout_height="1dp" android:visibility="gone">
            <com.google.android.material.card.MaterialCardView android:id="@+id/test_proxy_button"
                android:layout_width="1dp" android:layout_height="1dp" />
            <com.google.android.material.card.MaterialCardView android:id="@+id/domain_lists_button"
                android:layout_width="1dp" android:layout_height="1dp" />
        </LinearLayout>
        <com.google.android.material.card.MaterialCardView android:id="@+id/strategy_button"
            android:layout_width="1dp" android:layout_height="1dp" android:visibility="gone">
            <LinearLayout android:layout_width="1dp" android:layout_height="1dp">
                <TextView android:id="@+id/strategy_button_name" android:layout_width="1dp" android:layout_height="1dp" />
                <TextView android:id="@+id/strategy_button_text" android:layout_width="1dp" android:layout_height="1dp" />
            </LinearLayout>
        </com.google.android.material.card.MaterialCardView>
    </LinearLayout>
</ScrollView>''', encoding="utf-8")

# Wire quick toggles to selected applications.
main_activity = APP / "src/main/java/io/github/romanvht/byedpi/activities/MainActivity.kt"
text = main_activity.read_text(encoding="utf-8")
marker = '        historyUtils = HistoryUtils(this)\n'
if marker not in text:
    raise SystemExit("MainActivity history marker not found")
switch_code = '''
        val targetDefaults = setOf(
            "com.google.android.youtube",
            "org.telegram.messenger",
            "org.telegram.messenger.web",
            "org.thunderdog.challegram",
            "com.whatsapp",
            "com.whatsapp.w4b",
            "com.instagram.android"
        )
        val prefEditor = getPreferences()
        if (!prefEditor.contains("selected_apps")) {
            prefEditor.edit { putStringSet("selected_apps", targetDefaults) }
        }
        if (!prefEditor.contains("applist_type")) {
            prefEditor.edit { putString("applist_type", "whitelist") }
        }

        fun bindAppSwitch(id: Int, packages: Set<String>) {
            val toggle = findViewById<com.google.android.material.switchmaterial.SwitchMaterial>(id)
            fun selectedNow(): MutableSet<String> =
                getPreferences().getStringSet("selected_apps", targetDefaults)?.toMutableSet()
                    ?: targetDefaults.toMutableSet()

            toggle.isChecked = packages.any { it in selectedNow() }
            toggle.setOnCheckedChangeListener { _, enabled ->
                val next = selectedNow()
                if (enabled) next.addAll(packages) else next.removeAll(packages)
                getPreferences().edit { putStringSet("selected_apps", next) }

                if (appStatus.first == AppStatus.Running) {
                    val mode = getPreferences().mode()
                    if (mode != Mode.VPN || VpnService.prepare(this@MainActivity) == null) {
                        ServiceManager.restart(this@MainActivity, mode)
                    }
                }
            }
        }

        bindAppSwitch(R.id.switch_youtube, setOf("com.google.android.youtube"))
        bindAppSwitch(R.id.switch_telegram, setOf(
            "org.telegram.messenger",
            "org.telegram.messenger.web",
            "org.thunderdog.challegram"
        ))
        bindAppSwitch(R.id.switch_whatsapp, setOf("com.whatsapp", "com.whatsapp.w4b"))
        bindAppSwitch(R.id.switch_instagram, setOf("com.instagram.android"))
'''
text = text.replace(marker, marker + switch_code, 1)

strategy_marker = '    private fun updateStrategyButton() {\n'
if strategy_marker not in text:
    raise SystemExit("updateStrategyButton marker not found")
text = text.replace(strategy_marker, strategy_marker + '''        binding.strategyButton.visibility = View.GONE
        binding.cmdButtonsRow.visibility = View.GONE
        return
''', 1)

text = text.replace(
    'binding.statusButtonCard.setCardBackgroundColor(ContextCompat.getColor(this, R.color.green_active))',
    'binding.statusButtonCard.setCardBackgroundColor(android.graphics.Color.parseColor("#0B1B2E"))'
)
main_activity.write_text(text, encoding="utf-8")

# Point source-code link to ShieldBreaker repo.
settings_xml = APP / "src/main/res/xml/main_settings.xml"
text = settings_xml.read_text(encoding="utf-8")
text = text.replace('android:data="https://github.com/romanvht/ByeDPIAndroid"', 'android:data="https://github.com/alekseypavlov345-boop/RKNShieldAndroid"')
settings_xml.write_text(text, encoding="utf-8")

print("ShieldBreaker patch applied")
