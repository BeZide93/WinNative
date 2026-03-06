package com.winlator.cmod;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.winlator.cmod.steam.SteamLoginActivity;
import com.winlator.cmod.steam.service.SteamService;

/**
 * Fragment that shows store sign-in / sign-out options for
 * Steam, Epic Games, GOG, and Amazon Games.
 */
public class StoresFragment extends Fragment {

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        if (getActivity() != null && ((AppCompatActivity) getActivity()).getSupportActionBar() != null) {
            ((AppCompatActivity) getActivity()).getSupportActionBar().setTitle(R.string.stores);
        }
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        LinearLayout layout = new LinearLayout(getContext());
        layout.setOrientation(LinearLayout.VERTICAL);
        int padding = dpToPx(24);
        layout.setPadding(padding, padding, padding, padding);

        // Title
        TextView title = new TextView(getContext());
        title.setText(R.string.stores);
        title.setTextSize(22);
        title.setTextColor(0xFFE6EDF3);
        title.setPadding(0, 0, 0, dpToPx(16));
        layout.addView(title);

        // Steam
        addStoreRow(layout, "Steam",
                SteamService.Companion.isLoggedIn(),
                v -> {
                    if (SteamService.Companion.isLoggedIn()) {
                        SteamService.Companion.logOut();
                        refreshView();
                    } else {
                        startActivity(new Intent(getContext(), SteamLoginActivity.class));
                    }
                });

        // Epic Games
        addStoreRow(layout, "Epic Games",
                false, // TODO: EpicService.isLoggedIn()
                v -> {
                    // TODO: Epic sign-in/out
                    android.widget.Toast.makeText(getContext(), "Epic Games integration coming soon", android.widget.Toast.LENGTH_SHORT).show();
                });

        // GOG
        addStoreRow(layout, "GOG",
                false, // TODO: GOGService.isLoggedIn()
                v -> {
                    // TODO: GOG sign-in/out
                    android.widget.Toast.makeText(getContext(), "GOG integration coming soon", android.widget.Toast.LENGTH_SHORT).show();
                });

        // Amazon Games
        addStoreRow(layout, "Amazon Games",
                false, // TODO: AmazonService.isLoggedIn()
                v -> {
                    // TODO: Amazon sign-in/out
                    android.widget.Toast.makeText(getContext(), "Amazon Games integration coming soon", android.widget.Toast.LENGTH_SHORT).show();
                });

        return layout;
    }

    @Override
    public void onResume() {
        super.onResume();
        refreshView();
    }

    private void refreshView() {
        if (getView() != null) {
            // Force recreation to reflect sign-in state changes
            getParentFragmentManager().beginTransaction()
                    .detach(this)
                    .attach(this)
                    .commit();
        }
    }

    private void addStoreRow(LinearLayout parent, String storeName, boolean isLoggedIn, View.OnClickListener onClick) {
        LinearLayout row = new LinearLayout(getContext());
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setPadding(0, dpToPx(8), 0, dpToPx(8));
        row.setGravity(android.view.Gravity.CENTER_VERTICAL);

        // Store name
        TextView nameView = new TextView(getContext());
        nameView.setText(storeName);
        nameView.setTextSize(16);
        nameView.setTextColor(0xFFE6EDF3);
        LinearLayout.LayoutParams nameParams = new LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f);
        nameView.setLayoutParams(nameParams);
        row.addView(nameView);

        // Status indicator
        TextView statusView = new TextView(getContext());
        statusView.setText(isLoggedIn ? "● Signed In" : "○ Not Signed In");
        statusView.setTextSize(12);
        statusView.setTextColor(isLoggedIn ? 0xFF57CBDE : 0xFF8B949E);
        statusView.setPadding(dpToPx(8), 0, dpToPx(12), 0);
        row.addView(statusView);

        // Sign In / Sign Out button
        Button button = new Button(getContext());
        button.setText(isLoggedIn ? "Sign Out" : "Sign In");
        button.setOnClickListener(onClick);
        button.setTextSize(13);
        row.addView(button);

        // Divider line
        View divider = new View(getContext());
        divider.setBackgroundColor(0xFF30363D);
        LinearLayout.LayoutParams divParams = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dpToPx(1));
        divParams.topMargin = dpToPx(8);

        parent.addView(row);
        parent.addView(divider, divParams);
    }

    private int dpToPx(int dp) {
        return (int) (dp * getResources().getDisplayMetrics().density);
    }
}
