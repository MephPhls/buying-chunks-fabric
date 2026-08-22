package snoopypupser.buyingchunks.mixin;

import net.minecraft.class_310;
import net.minecraft.class_312;
import org.lwjgl.glfw.GLFW;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import snoopypupser.buyingchunks.client.BuyableChunkOverlay;

/**
 * Handles clicks on the HUD overlay.
 * Minecraft 1.21.1 MouseHandler#onPress is intermediary method_1601.
 */
@Mixin(class_312.class)
public class MouseHandlerMixin {
    @Inject(method = "method_1601", at = @At("HEAD"), cancellable = true, remap = false)
    private void buyingchunks$clickOverlay(long window, int button, int action, int mods, CallbackInfo ci) {
        if (button != GLFW.GLFW_MOUSE_BUTTON_1 || action != GLFW.GLFW_PRESS || !BuyableChunkOverlay.isActive()) return;
        class_310 mc = class_310.method_1551();
        double mx = mc.field_1729.method_1603() * mc.method_22683().method_4486() / mc.method_22683().method_4480();
        double my = mc.field_1729.method_1604() * mc.method_22683().method_4502() / mc.method_22683().method_4507();
        if (BuyableChunkOverlay.handleClick(mx, my)) ci.cancel();
    }
}
