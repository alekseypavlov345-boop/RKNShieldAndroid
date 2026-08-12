package com.rknshield.android;

import android.app.Activity;
import android.content.Intent;
import android.net.VpnService;
import android.os.Bundle;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;

import com.wireguard.android.backend.GoBackend;
import com.wireguard.android.backend.Tunnel;
import com.wireguard.config.Config;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.ByteArrayOutputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class MainActivity extends AppCompatActivity {
    private final ExecutorService executor = Executors.newSingleThreadExecutor();
    private final RknTunnel tunnel = new RknTunnel();

    private GoBackend backend;
    private Button toggleButton;
    private TextView statusText;
    private TextView configStatusText;
    private CheckBox telegramCheck;
    private CheckBox whatsappCheck;
    private CheckBox instagramCheck;
    private CheckBox youtubeCheck;
    private volatile boolean isUp = false;

    private final ActivityResultLauncher<Intent> vpnPermissionLauncher =
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() == Activity.RESULT_OK) {
                    connectTunnel();
                } else {
                    setStatus("Android не выдал разрешение VPN", false);
                }
            });

    private final ActivityResultLauncher<Intent> configPickerLauncher =
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() != Activity.RESULT_OK || result.getData() == null) return;
                if (result.getData().getData() == null) return;

                try (InputStream input = getContentResolver().openInputStream(result.getData().getData())) {
                    if (input == null) throw new IOException("Не удалось открыть файл");
                    ByteArrayOutputStream buffer = new ByteArrayOutputStream();
                    byte[] chunk = new byte[8192];
                    int count;
                    while ((count = input.read(chunk)) != -1) {
                        buffer.write(chunk, 0, count);
                    }
                    String configText = new String(buffer.toByteArray(), StandardCharsets.UTF_8);
                    Config.parse(new ByteArrayInputStream(configText.getBytes(StandardCharsets.UTF_8)));
                    ConfigStore.save(this, configText);
                    configStatusText.setText("Конфигурация загружена");
                    Toast.makeText(this, "WireGuard конфигурация сохранена", Toast.LENGTH_SHORT).show();
                } catch (Exception e) {
                    showError("Ошибка конфигурации: " + safeMessage(e));
                }
            });

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        backend = new GoBackend(getApplicationContext());
        toggleButton = findViewById(R.id.toggleButton);
        statusText = findViewById(R.id.statusText);
        configStatusText = findViewById(R.id.configStatusText);
        telegramCheck = findViewById(R.id.telegramCheck);
        whatsappCheck = findViewById(R.id.whatsappCheck);
        instagramCheck = findViewById(R.id.instagramCheck);
        youtubeCheck = findViewById(R.id.youtubeCheck);

        configureAppCheckbox(telegramCheck, AppTargets.TELEGRAM);
        configureAppCheckbox(whatsappCheck, AppTargets.WHATSAPP);
        configureAppCheckbox(instagramCheck, AppTargets.INSTAGRAM);
        configureAppCheckbox(youtubeCheck, AppTargets.YOUTUBE);

        configStatusText.setText(ConfigStore.exists(this)
                ? "Конфигурация загружена"
                : "Конфигурация не загружена");

        findViewById(R.id.importConfigButton).setOnClickListener(v -> openConfigPicker());
        toggleButton.setOnClickListener(v -> {
            if (isUp) {
                disconnectTunnel();
            } else {
                requestVpnAndConnect();
            }
        });
    }

    private void configureAppCheckbox(CheckBox checkBox, String[] candidates) {
        boolean installed = !AppTargets.installedPackages(this, candidates).isEmpty();
        checkBox.setEnabled(installed);
        checkBox.setChecked(installed);
        if (!installed) {
            checkBox.setText(checkBox.getText() + " — не установлено");
        }
    }

    private void openConfigPicker() {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType("*/*");
        configPickerLauncher.launch(intent);
    }

    private void requestVpnAndConnect() {
        if (!ConfigStore.exists(this)) {
            showError("Сначала импортируй WireGuard .conf");
            return;
        }

        Intent prepareIntent = VpnService.prepare(this);
        if (prepareIntent != null) {
            vpnPermissionLauncher.launch(prepareIntent);
        } else {
            connectTunnel();
        }
    }

    private List<String> selectedInstalledPackages() {
        List<String> packages = new ArrayList<>();
        if (telegramCheck.isChecked()) packages.addAll(AppTargets.installedPackages(this, AppTargets.TELEGRAM));
        if (whatsappCheck.isChecked()) packages.addAll(AppTargets.installedPackages(this, AppTargets.WHATSAPP));
        if (instagramCheck.isChecked()) packages.addAll(AppTargets.installedPackages(this, AppTargets.INSTAGRAM));
        if (youtubeCheck.isChecked()) packages.addAll(AppTargets.installedPackages(this, AppTargets.YOUTUBE));
        return packages;
    }

    private void connectTunnel() {
        List<String> selected = selectedInstalledPackages();
        if (selected.isEmpty()) {
            showError("Выбери хотя бы одно установленное приложение");
            return;
        }

        setBusy(true, "Подключение…");
        executor.execute(() -> {
            try {
                String rawConfig = ConfigStore.load(this);
                String scopedConfig = WireGuardConfigTools.withIncludedApplications(rawConfig, selected);
                Config config = Config.parse(new ByteArrayInputStream(scopedConfig.getBytes(StandardCharsets.UTF_8)));
                Tunnel.State state = backend.setState(tunnel, Tunnel.State.UP, config);
                isUp = state == Tunnel.State.UP;
                runOnUiThread(() -> {
                    setBusy(false, isUp ? "Обход включён" : "Не удалось включить обход");
                    updateButton();
                });
            } catch (Exception e) {
                isUp = false;
                runOnUiThread(() -> {
                    setBusy(false, "Ошибка подключения");
                    updateButton();
                    showError("Не удалось подключиться: " + safeMessage(e));
                });
            }
        });
    }

    private void disconnectTunnel() {
        setBusy(true, "Отключение…");
        executor.execute(() -> {
            try {
                backend.setState(tunnel, Tunnel.State.DOWN, null);
                isUp = false;
                runOnUiThread(() -> {
                    setBusy(false, "Обход выключен");
                    updateButton();
                });
            } catch (Exception e) {
                runOnUiThread(() -> {
                    setBusy(false, "Ошибка отключения");
                    showError("Не удалось отключить: " + safeMessage(e));
                });
            }
        });
    }

    private void updateButton() {
        toggleButton.setText(isUp ? "ОБХОД ВЫКЛ" : "ОБХОД ВКЛ");
    }

    private void setBusy(boolean busy, String text) {
        toggleButton.setEnabled(!busy);
        statusText.setText(text);
    }

    private void setStatus(String text, boolean up) {
        isUp = up;
        statusText.setText(text);
        updateButton();
    }

    private void showError(String message) {
        statusText.setText(message);
        Toast.makeText(this, message, Toast.LENGTH_LONG).show();
    }

    private static String safeMessage(Throwable t) {
        return t.getMessage() == null ? t.getClass().getSimpleName() : t.getMessage();
    }

    @Override
    protected void onDestroy() {
        executor.shutdown();
        super.onDestroy();
    }
}
