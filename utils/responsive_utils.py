# -*- coding: utf-8 -*-
"""
Responsive Utilities for Dynamic UI Scaling
Provides automatic DPI detection and element scaling for responsive design
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSize
import sys


class ResponsiveHelper:
    """Helper class for responsive UI scaling based on screen DPI and resolution"""
    
    def __init__(self):
        """Initialize responsive helper with current screen metrics"""
        self._update_screen_metrics()
    
    def _update_screen_metrics(self):
        """Update screen metrics (DPI, resolution, scale factor)"""
        try:
            screen = QApplication.primaryScreen()
            if screen:
                # Get physical DPI
                self.physical_dpi = screen.physicalDotsPerInch()
                self.logical_dpi = screen.logicalDotsPerInch()
                
                # Get screen geometry
                geometry = screen.geometry()
                self.screen_width = geometry.width()
                self.screen_height = geometry.height()
                
                # Calculate device pixel ratio (for high-DPI displays)
                self.device_pixel_ratio = screen.devicePixelRatio()
                
                # Calculate scale factor based on DPI
                # Standard DPI is 96 on Windows, 72 on Mac
                base_dpi = 96.0
                self.dpi_scale_factor = self.logical_dpi / base_dpi
                
                # Adjust scale factor based on screen resolution
                # For very high resolutions, we might want to scale up more
                if self.screen_width >= 3840:  # 4K or higher
                    self.resolution_multiplier = 1.2
                elif self.screen_width >= 2560:  # QHD
                    self.resolution_multiplier = 1.1
                elif self.screen_width >= 1920:  # Full HD
                    self.resolution_multiplier = 1.0
                elif self.screen_width >= 1366:  # HD
                    self.resolution_multiplier = 0.9
                else:  # Ultra low (1280 or less)
                    self.resolution_multiplier = 0.85
                
                # Special multiplier for vertical space (important for 720p)
                if self.screen_height <= 800:
                    self.height_multiplier = 0.8  # Aggressive reduction for low height
                else:
                    self.height_multiplier = 1.0
                
                # Combined scale factor for general sizes
                self.scale_factor = self.dpi_scale_factor * self.resolution_multiplier
                
                # Dedicated factor for vertical elements, spacing and margins
                self.vertical_scale_factor = self.scale_factor * self.height_multiplier
                
                # Clamp scale factor to reasonable range
                self.scale_factor = max(0.8, min(2.0, self.scale_factor))
                self.vertical_scale_factor = max(0.7, min(2.0, self.vertical_scale_factor))
                
            else:
                # Fallback values if screen is not available
                self._set_fallback_values()
        except Exception as e:
            print(f"Error detecting screen metrics: {e}")
            self._set_fallback_values()
    
    def _set_fallback_values(self):
        """Set fallback values when screen detection fails"""
        self.physical_dpi = 96
        self.logical_dpi = 96
        self.screen_width = 1920
        self.screen_height = 1080
        self.device_pixel_ratio = 1.0
        self.dpi_scale_factor = 1.0
        self.resolution_multiplier = 1.0
        self.scale_factor = 1.0
    
    def get_dpi_scale_factor(self):
        """
        Get the DPI scale factor
        
        Returns:
            float: Scale factor based on screen DPI (typically 1.0 to 2.0)
        """
        return self.dpi_scale_factor
    
    def get_combined_scale_factor(self):
        """
        Get the combined scale factor (DPI + resolution)
        
        Returns:
            float: Combined scale factor
        """
        return self.scale_factor
    
    def scale_size(self, base_size):
        """
        Scale a size value based on screen metrics
        
        Args:
            base_size (int): Base size in pixels (at 96 DPI, 1920x1080)
        
        Returns:
            int: Scaled size in pixels
        """
        return int(base_size * self.scale_factor)
    
    def scale_font_size(self, base_font_size):
        """
        Scale a font size based on screen metrics
        
        Args:
            base_font_size (int): Base font size in pixels
        
        Returns:
            int: Scaled font size in pixels
        """
        # Font scaling is slightly less aggressive than general scaling
        font_scale = max(0.9, min(1.5, self.scale_factor))
        return int(base_font_size * font_scale)
    
    def get_responsive_button_size(self, base_width, base_height):
        """
        Get responsive button size
        
        Args:
            base_width (int): Base button width
            base_height (int): Base button height
        
        Returns:
            QSize: Scaled button size
        """
        width = self.scale_size(base_width)
        height = self.scale_size(base_height)
        return QSize(width, height)
    
    def get_responsive_spacing(self, base_spacing=12):
        """
        Get responsive spacing for layouts
        
        Args:
            base_spacing (int): Base spacing in pixels (default: 12)
        
        Returns:
            int: Scaled spacing
        """
        return int(base_spacing * self.vertical_scale_factor)
    
    def get_responsive_margins(self, base_margin=16):
        """
        Get responsive margins for layouts
        
        Args:
            base_margin (int): Base margin in pixels (default: 16)
        
        Returns:
            int: Scaled margin
        """
        return int(base_margin * self.vertical_scale_factor)
    
    def get_responsive_icon_size(self, base_size=24):
        """
        Get responsive icon size
        
        Args:
            base_size (int): Base icon size in pixels (default: 24)
        
        Returns:
            int: Scaled icon size
        """
        return self.scale_size(base_size)
    
    def get_screen_dpi(self):
        """
        Get screen DPI
        
        Returns:
            float: Screen DPI
        """
        return self.logical_dpi
    
    def get_screen_resolution(self):
        """
        Get screen resolution
        
        Returns:
            tuple: (width, height) in pixels
        """
        return (self.screen_width, self.screen_height)
    
    def is_high_dpi(self):
        """
        Check if display is high DPI
        
        Returns:
            bool: True if DPI > 120
        """
        return self.logical_dpi > 120
    
    def is_4k_or_higher(self):
        """
        Check if display is 4K or higher resolution
        
        Returns:
            bool: True if width >= 3840
        """
        return self.screen_width >= 3840
    
    def get_optimal_figure_size(self, container_width=None, container_height=None):
        """
        Calculate optimal matplotlib figure size in inches
        
        Args:
            container_width (int): Container width in pixels (optional)
            container_height (int): Container height in pixels (optional)
        
        Returns:
            tuple: (width_inches, height_inches)
        """
        dpi = self.get_screen_dpi()
        
        if container_width is None:
            # Default to reasonable size based on screen
            container_width = int(self.screen_width * 0.4)
        
        if container_height is None:
            container_height = int(self.screen_height * 0.3)
        
        # Convert pixels to inches
        width_inches = container_width / dpi
        height_inches = container_height / dpi
        
        return (width_inches, height_inches)
    
    def refresh_metrics(self):
        """Refresh screen metrics (call after screen change or window move)"""
        self._update_screen_metrics()
    
    def get_debug_info(self):
        """
        Get debug information about current scaling
        
        Returns:
            dict: Debug information
        """
        return {
            'physical_dpi': self.physical_dpi,
            'logical_dpi': self.logical_dpi,
            'screen_resolution': f'{self.screen_width}x{self.screen_height}',
            'device_pixel_ratio': self.device_pixel_ratio,
            'dpi_scale_factor': self.dpi_scale_factor,
            'resolution_multiplier': self.resolution_multiplier,
            'combined_scale_factor': self.scale_factor,
            'is_high_dpi': self.is_high_dpi(),
            'is_4k': self.is_4k_or_higher()
        }


# Singleton instance for easy access
_responsive_helper_instance = None

def get_responsive_helper():
    """
    Get singleton instance of ResponsiveHelper
    
    Returns:
        ResponsiveHelper: Singleton instance
    """
    global _responsive_helper_instance
    if _responsive_helper_instance is None:
        _responsive_helper_instance = ResponsiveHelper()
    return _responsive_helper_instance


# Convenience functions
def scale(size):
    """Convenience function to scale a size"""
    return get_responsive_helper().scale_size(size)

def scale_font(size):
    """Convenience function to scale a font size"""
    return get_responsive_helper().scale_font_size(size)

def spacing():
    """Convenience function to get responsive spacing"""
    return get_responsive_helper().get_responsive_spacing()

def margins():
    """Convenience function to get responsive margins"""
    return get_responsive_helper().get_responsive_margins()
