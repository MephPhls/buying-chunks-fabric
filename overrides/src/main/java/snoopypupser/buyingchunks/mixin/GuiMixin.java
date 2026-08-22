package snoopypupser.buyingchunks.mixin;

import net.minecraft.class_329;
import net.minecraft.class_332;
import net.minecraft.class_9779;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import snoopypupser.buyingchunks.client.BuyableChunkOverlay;

/**
 * Renders the Buying Chunks HUD overlay after vanilla HUD rendering.
 *
 * The Fabric runtime uses intermediary Minecraft names. Because this project
 * intentionally ships without a refmap, the injection target must also use
 * the intermediary method name. In Minecraft 1.21.1 Gui#render is method_1753.
 */
@Mixin(class_329.class)
public class GuiMixin {

    @Inject(method = "method_1753", at = @At("TAIL"), remap = false)
    private void buyingchunks$onRender(class_332 guiGraphics, class_9779 deltaTracker, CallbackInfo ci) {
        BuyableChunkOverlay.render(guiGraphics);
    }
}
