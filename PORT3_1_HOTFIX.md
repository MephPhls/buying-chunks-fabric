# Port3.1 hotfix

Corrige los mixins cliente que apuntaban a nombres `named` sin refmap. En Minecraft/Fabric 1.21.1 se usan los targets intermediary `method_1753` para `Gui#render` y `method_1601` para `MouseHandler#onPress`.
