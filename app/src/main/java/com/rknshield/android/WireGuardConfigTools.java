package com.rknshield.android;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

final class WireGuardConfigTools {
    private WireGuardConfigTools() {}

    static String withIncludedApplications(String original, List<String> packages) {
        if (packages.isEmpty()) {
            throw new IllegalArgumentException("Не выбрано ни одного установленного приложения");
        }

        String normalized = original.replace("\r\n", "\n").replace('\r', '\n');
        String[] lines = normalized.split("\n", -1);
        List<String> out = new ArrayList<>();
        boolean interfaceSeen = false;
        boolean inserted = false;

        for (String line : lines) {
            String trimmed = line.trim();
            String lower = trimmed.toLowerCase(Locale.ROOT);

            if (lower.equals("[interface]")) {
                interfaceSeen = true;
            }

            if (lower.startsWith("includedapplications") || lower.startsWith("excludedapplications")) {
                continue;
            }

            if (!inserted && interfaceSeen && lower.equals("[peer]")) {
                out.add("IncludedApplications = " + String.join(", ", packages));
                inserted = true;
            }

            out.add(line);
        }

        if (!interfaceSeen) {
            throw new IllegalArgumentException("В конфигурации отсутствует секция [Interface]");
        }

        if (!inserted) {
            out.add("IncludedApplications = " + String.join(", ", packages));
        }

        return String.join("\n", out);
    }
}
