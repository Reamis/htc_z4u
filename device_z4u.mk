$(call inherit-product, $(SRC_TARGET_DIR)/product/languages_full.mk)

# The gps config appropriate for this device
$(call inherit-product, device/common/gps/gps_us_supl.mk)

$(call inherit-product-if-exists, vendor/htc/z4u/z4u-vendor.mk)

DEVICE_PACKAGE_OVERLAYS += device/htc/z4u/overlay

#LOCAL_PATH := device/htc/z4u
#ifeq ($(TARGET_PREBUILT_KERNEL),)
#	LOCAL_KERNEL := $(LOCAL_PATH)/kernel
#else
#	LOCAL_KERNEL := $(TARGET_PREBUILT_KERNEL)
#endif

#PRODUCT_COPY_FILES += \
#    $(LOCAL_KERNEL):kernel

TARGET_KERNEL_SOURCE := kernel/htc/z4u
TARGET_KERNEL_CONFIG := z4u_defconfig

$(call inherit-product, build/target/product/full.mk)

PRODUCT_BUILD_PROP_OVERRIDES += BUILD_UTC_DATE=0
PRODUCT_NAME := full_z4u
PRODUCT_DEVICE := z4u
