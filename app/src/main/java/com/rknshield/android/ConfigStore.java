package com.rknshield.android;

import android.content.Context;

import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

final class ConfigStore {
    private static final String FILE_NAME = "wireguard.conf";

    private ConfigStore() {}

    static void save(Context context, String config) throws IOException {
        try (OutputStream output = context.openFileOutput(FILE_NAME, Context.MODE_PRIVATE)) {
            output.write(config.getBytes(StandardCharsets.UTF_8));
        }
    }

    static String load(Context context) throws IOException {
        try (InputStream input = context.openFileInput(FILE_NAME)) {
            ByteArrayOutputStream output = new ByteArrayOutputStream();
            byte[] buffer = new byte[8192];
            int read;
            while ((read = input.read(buffer)) != -1) {
                output.write(buffer, 0, read);
            }
            return output.toString(StandardCharsets.UTF_8.name());
        } catch (FileNotFoundException e) {
            throw new IOException("Конфигурация WireGuard не загружена", e);
        }
    }

    static boolean exists(Context context) {
        return context.getFileStreamPath(FILE_NAME).exists();
    }
}
