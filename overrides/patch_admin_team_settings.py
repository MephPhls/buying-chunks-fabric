from pathlib import Path

p = Path('src/main/java/snoopypupser/buyingchunks/client/AdminServerTeamDetailScreen.java')
s = p.read_text()

s = s.replace('''    private static final String[] PRIVACY_KEYS = {
        "block_edit_mode", "block_interact_mode", "entity_interact_mode",
        "nonliving_entity_attack_mode", "claim_visibility", "location_mode",
        "block_edit_and_interact_mode"
    };''', '''    // Fabric uses one combined block edit/interact property. The separate edit/interact
    // properties are Forge-side settings and are intentionally not shown here.
    private static final String[] PRIVACY_KEYS = {
        "entity_interact_mode", "nonliving_entity_attack_mode",
        "claim_visibility", "location_mode", "block_edit_and_interact_mode"
    };''')

s = s.replace('''    private int deleteX, chunkX;
''', '''    private int deleteX, chunkX;

    // FTB Chunks protection properties are not sync-to-all in FTB Teams. Server
    // teams have no members, so the admin client's Team object won't refresh
    // after a change. Keep an editable local copy and commit it with Save.
    private final boolean[] pendingBoolValues = new boolean[BOOL_KEYS.length];
    private final PrivacyMode[] pendingPrivacyValues = new PrivacyMode[PRIVACY_KEYS.length];
''')

s = s.replace('''        try { c = team.getProperty(dev.ftb.mods.ftbteams.api.property.TeamProperties.COLOR).rgb(); } catch (Exception ignored) {}
        this.teamColor = c;
    }
''', '''        try { c = team.getProperty(dev.ftb.mods.ftbteams.api.property.TeamProperties.COLOR).rgb(); } catch (Exception ignored) {}
        this.teamColor = c;

        for (int i = 0; i < BOOL_KEYS.length; i++) {
            pendingBoolValues[i] = readBoolPropFromTeam(BOOL_KEYS[i]);
        }
        for (int i = 0; i < PRIVACY_KEYS.length; i++) {
            pendingPrivacyValues[i] = readPrivacyPropFromTeam(PRIVACY_KEYS[i]);
        }
    }
''')

s = s.replace('boolean val = readBoolProp(BOOL_KEYS[i]);', 'boolean val = pendingBoolValues[i];')
s = s.replace('PrivacyMode mode = readPrivacyProp(PRIVACY_KEYS[i]);', 'PrivacyMode mode = pendingPrivacyValues[i];')
s = s.replace('private boolean readBoolProp(String key) {', 'private boolean readBoolPropFromTeam(String key) {')
s = s.replace('private PrivacyMode readPrivacyProp(String key) {', 'private PrivacyMode readPrivacyPropFromTeam(String key) {')

old_mutators = '''    private void toggleBoolProp(int index) {
        String key = BOOL_KEYS[index];
        boolean current = readBoolProp(key);
        snoopypupser.buyingchunks.network.BuyingChunksClientNetwork.sendToServer(new AdminActionPacket(
                AdminActionPacket.ACTION_SET_BOOL_PROPERTY, team.getId(), key, 0, !current, AdminActionPacket.NO_DIMENSION));
    }

    private void cyclePrivacyProp(int index) {
        String key = PRIVACY_KEYS[index];
        PrivacyMode current = readPrivacyProp(key);
        int nextOrd = (current.ordinal() + 1) % PRIVACY_VALUES.length;
        PrivacyMode next = PRIVACY_VALUES[nextOrd];
        snoopypupser.buyingchunks.network.BuyingChunksClientNetwork.sendToServer(new AdminActionPacket(
                AdminActionPacket.ACTION_SET_PRIVACY_PROPERTY, team.getId(), key + "=" + next.name(), 0, false, AdminActionPacket.NO_DIMENSION));
    }
'''
new_mutators = '''    private void toggleBoolProp(int index) {
        pendingBoolValues[index] = !pendingBoolValues[index];
    }

    private void cyclePrivacyProp(int index) {
        PrivacyMode current = pendingPrivacyValues[index];
        int nextOrd = (current.ordinal() + 1) % PRIVACY_VALUES.length;
        pendingPrivacyValues[index] = PRIVACY_VALUES[nextOrd];
    }

    private void applyLocalBoolProp(String key, boolean value) {
        try {
            switch (key) {
                case "allow_explosions" -> team.setProperty(FTBChunksProperties.ALLOW_EXPLOSIONS, value);
                case "allow_mob_griefing" -> team.setProperty(FTBChunksProperties.ALLOW_MOB_GRIEFING, value);
                case "allow_pvp" -> team.setProperty(FTBChunksProperties.ALLOW_PVP, value);
                case "allow_all_fake_players" -> team.setProperty(FTBChunksProperties.ALLOW_ALL_FAKE_PLAYERS, value);
                case "allow_fake_players_by_id" -> team.setProperty(FTBChunksProperties.ALLOW_FAKE_PLAYERS_BY_ID, value);
            }
        } catch (Exception e) {
            BuyingChunks.LOGGER.warn("AdminServerTeamDetailScreen: failed to update local boolean property {}", key, e);
        }
    }

    private void applyLocalPrivacyProp(String key, PrivacyMode value) {
        try {
            switch (key) {
                case "entity_interact_mode" -> team.setProperty(FTBChunksProperties.ENTITY_INTERACT_MODE, value);
                case "nonliving_entity_attack_mode" -> team.setProperty(FTBChunksProperties.NONLIVING_ENTITY_ATTACK_MODE, value);
                case "claim_visibility" -> team.setProperty(FTBChunksProperties.CLAIM_VISIBILITY, value);
                case "location_mode" -> team.setProperty(FTBChunksProperties.LOCATION_MODE, value);
                case "block_edit_and_interact_mode" -> team.setProperty(FTBChunksProperties.BLOCK_EDIT_AND_INTERACT_MODE, value);
            }
        } catch (Exception e) {
            BuyingChunks.LOGGER.warn("AdminServerTeamDetailScreen: failed to update local privacy property {}", key, e);
        }
    }
'''
if old_mutators not in s:
    raise SystemExit('Port4 admin-team mutator block not found')
s = s.replace(old_mutators, new_mutators)

old_save = '''    private void doSaveAll() {
        String hex = colorField.getText().trim();
        if (!hex.isEmpty()) {
            try {
                int rgb = Integer.parseInt(hex, 16);
                snoopypupser.buyingchunks.network.BuyingChunksClientNetwork.sendToServer(new AdminActionPacket(
                        AdminActionPacket.ACTION_UPDATE_TEAM_COLOR, team.getId(), "", rgb, false, AdminActionPacket.NO_DIMENSION));
            } catch (NumberFormatException ignored) {}
        }
    }
'''
new_save = '''    private void doSaveAll() {
        String hex = colorField.getText().trim();
        if (!hex.isEmpty()) {
            try {
                int rgb = Integer.parseInt(hex, 16);
                snoopypupser.buyingchunks.network.BuyingChunksClientNetwork.sendToServer(new AdminActionPacket(
                        AdminActionPacket.ACTION_UPDATE_TEAM_COLOR, team.getId(), "", rgb, false, AdminActionPacket.NO_DIMENSION));
            } catch (NumberFormatException ignored) {}
        }

        for (int i = 0; i < BOOL_KEYS.length; i++) {
            String key = BOOL_KEYS[i];
            boolean value = pendingBoolValues[i];
            snoopypupser.buyingchunks.network.BuyingChunksClientNetwork.sendToServer(new AdminActionPacket(
                    AdminActionPacket.ACTION_SET_BOOL_PROPERTY, team.getId(), key, 0, value, AdminActionPacket.NO_DIMENSION));
            applyLocalBoolProp(key, value);
        }

        for (int i = 0; i < PRIVACY_KEYS.length; i++) {
            String key = PRIVACY_KEYS[i];
            PrivacyMode value = pendingPrivacyValues[i];
            snoopypupser.buyingchunks.network.BuyingChunksClientNetwork.sendToServer(new AdminActionPacket(
                    AdminActionPacket.ACTION_SET_PRIVACY_PROPERTY, team.getId(),
                    key + "=" + value.name(), 0, false, AdminActionPacket.NO_DIMENSION));
            applyLocalPrivacyProp(key, value);
        }

        if (class_310.method_1551().field_1724 != null) {
            class_310.method_1551().field_1724.method_43496(
                    BuyingChunks.prefix(class_2561.method_43470("Configuración del equipo guardada.")));
        }
    }
'''
if old_save not in s:
    raise SystemExit('Port4 admin-team save block not found')
s = s.replace(old_save, new_save)

p.write_text(s)
