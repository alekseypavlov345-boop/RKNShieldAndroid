package com.rknshield.android;

import android.content.Context;
import android.content.pm.PackageManager;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

final class AppTargets {
    private AppTargets() {}

    static final String[] TELEGRAM = {
            "org.telegram.messenger",
            "org.telegram.messenger.web",
            "org.thunderdog.challegram"
    };

    static final String[] WHATSAPP = {
            "com.whatsapp",
            "com.whatsapp.w4b"
    };

    static final String[] INSTAGRAM = {
            "com.instagram.android"
    };

    static final String[] YOUTUBE = {
            "com.google.android.youtube"
    };

    @SuppressWarnings("deprecation")
    static List<String> installedPackages(Context context, String[] candidates) {
        PackageManager pm = context.getPackageManager();
        List<String> result = new ArrayList<>();
        for (String packageName : candidates) {
            try {
                pm.getPackageInfo(packageName, 0);
                result.add(packageName);
            } catch (PackageManager.NameNotFoundException ignored) {
                // Not installed.
            }
        }
        return Collections.unmodifiableList(result);
    }
}
