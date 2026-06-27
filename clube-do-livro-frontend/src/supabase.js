import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

// Cria o robô de conexão pronto para ser usado em qualquer lugar do app
export const supabase = createClient(supabaseUrl, supabaseAnonKey)