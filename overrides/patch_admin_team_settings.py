from pathlib import Path

p = Path('src/main/java/snoopypupser/buyingchunks/client/AdminServerTeamDetailScreen.java')
s = p.read_text()

# Fabric uses the combined block-edit/interact property. The two separate
# Forge-side properties are misleading here and don't control Fabric protection.
s = s.replace('''    private static final String[] PRIVACY_KEYS = {
        "block_edit_mode", "block_interact_mode", "entity_interact_mode",
        "nonliving_entity_attack_mode", "claim_visibility", "location_mode",
        "block_edit_and_interact_mode"
    };''', '''    private static final String[] PRIVACY_KEYS = {
        "entity_interact_mode", "nonliving_entity_attack_mode",
        "claim_visibility", "location_mode", "block_edit_and_interact_mode"
    };''')

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
        String key = BOOL_KEYS[index];
        boolean next = !readBoolProp(key);
        snoopypupser.buyingchunks.network.BuyingChunksClientNetwork.sendToServer(new AdminActionPacket(
                AdminActionPacket.ACTION_SET_BOOL_PROPERTY, team.getId(), key, 0, next, AdminActionPacket.NO_DIMENSION));
        applyLocalBoolProp(key, next);
    }

    private void cyclePrivacyProp(int index) {
        String key = PRIVACY_KEYS[index];
        PrivacyMode current = readPrivacyProp(key);
        int nextOrd = (current.ordinal() + 1) % PRIVACY_VALUES.length;
        PrivacyMode next = PRIVACY_VALUES[nextOrd];
        snoopypupser.buyingchunks.network.BuyingChunksClientNetwork.sendToServer(new AdminActionPacket(
                AdminActionPacket.ACTION_SET_PRIVACY_PROPERTY, team.getId(), key + "=" + next.name(), 0, false, AdminActionPacket.NO_DIMENSION));
        applyLocalPrivacyProp(key, next);
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
            BuyingChunks.LOGGER.warn("AdminServerTeamDetailScreen: failed to mirror local boolean property {}", key, e);
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
            BuyingChunks.LOGGER.warn("AdminServerTeamDetailScreen: failed to mirror local privacy property {}", key, e);
        }
    }
'''
if old_mutators not in s:
    raise SystemExit('Port4 admin-team mutator block not found')
s = s.replace(old_mutators, new_mutators)

p.write_text(s)
