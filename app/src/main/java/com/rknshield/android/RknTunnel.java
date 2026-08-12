package com.rknshield.android;

import com.wireguard.android.backend.Tunnel;

final class RknTunnel implements Tunnel {
    private volatile State state = State.DOWN;

    @Override
    public String getName() {
        return "rknshield";
    }

    @Override
    public void onStateChange(State newState) {
        state = newState;
    }

    State getState() {
        return state;
    }
}
