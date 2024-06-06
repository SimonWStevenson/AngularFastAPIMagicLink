export interface Session {
    email: string;
    id: number;
    created_date: string;
    user_id: number;
    browser: string;
    browser_version: string;
    os: string;
    os_version: string;
    device: string;
    device_brand: string;
    device_model: string;
    is_mobile: boolean;
    is_tablet: boolean;
    is_pc: boolean;
    is_bot: boolean;
    is_this_session: boolean;
  }