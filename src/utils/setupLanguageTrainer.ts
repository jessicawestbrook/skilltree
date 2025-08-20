import { createLanguageTrainerTables, checkLanguageTrainerTables } from './createLanguageTrainerTables'

export async function setupLanguageTrainer() {
  try {
    console.log('Checking if Language Trainer tables exist...')
    const tablesExist = await checkLanguageTrainerTables()
    
    if (!tablesExist) {
      console.log('Language Trainer tables do not exist. Creating tables...')
      const success = await createLanguageTrainerTables()
      
      if (success) {
        console.log('✅ Language Trainer tables created successfully!')
        return true
      } else {
        console.error('❌ Failed to create Language Trainer tables')
        return false
      }
    } else {
      console.log('✅ Language Trainer tables already exist')
      return true
    }
  } catch (error) {
    console.error('Error setting up Language Trainer:', error)
    return false
  }
}